const DATA_URL = "../database_with_routes.json";
const SVG_URL = "assets/bfw-eg-ost.svg";
const SVG_NS = "http://www.w3.org/2000/svg";

const form = document.querySelector("#route-form");
const startSelect = document.querySelector("#start-zone");
const targetSelect = document.querySelector("#target-zone");
const swapButton = document.querySelector("#swap-zones");
const modelStatus = document.querySelector("#model-status");
const floorPlan = document.querySelector("#floor-plan");
const routeSegments = document.querySelector("#route-segments");
const routeMarkers = document.querySelector("#route-markers");
const routeSummary = document.querySelector("#route-summary");
const routeDistance = document.querySelector("#route-distance");
const routePortalCount = document.querySelector("#route-portal-count");
const routeCost = document.querySelector("#route-cost");
const instructionList = document.querySelector("#instruction-list");
const emptyState = document.querySelector("#empty-state");
const canonicalRoute = document.querySelector("#canonical-route");
const stateChain = document.querySelector("#state-chain");

let database = null;

function zoneLabel(zoneId) {
    const zone = database.zones[zoneId];
    return zone.label === zoneId ? zoneId : `${zoneId} · ${zone.label}`;
}

function sortedDestinationZones() {
    return Object.values(database.zones)
        .sort((left, right) => left.id.localeCompare(right.id, "de", { numeric: true }));
}

function populateSelect(select, zones) {
    const fragment = document.createDocumentFragment();
    for (const zone of zones) {
        const option = document.createElement("option");
        option.value = zone.id;
        option.textContent = zoneLabel(zone.id);
        fragment.appendChild(option);
    }
    select.replaceChildren(fragment);
}

async function loadPrototype() {
    try {
        const [dataResponse, svgResponse] = await Promise.all([fetch(DATA_URL), fetch(SVG_URL)]);
        if (!dataResponse.ok || !svgResponse.ok) {
            throw new Error(`Daten ${dataResponse.status}, SVG ${svgResponse.status}`);
        }
        database = await dataResponse.json();
        floorPlan.innerHTML = await svgResponse.text();
        const zones = sortedDestinationZones();
        populateSelect(startSelect, zones);
        populateSelect(targetSelect, zones);
        startSelect.value = "E.61";
        targetSelect.value = "E.57";
        modelStatus.textContent = `${Object.keys(database.zones).length} Zonen · ${Object.keys(database.portals).length} Portale · ${database.meta.route_count} Routen`;
        renderSelectedRoute();
    } catch (error) {
        modelStatus.textContent = "Prototypdaten konnten nicht geladen werden";
        modelStatus.setAttribute("data-error", "true");
        emptyState.textContent = "Die Seite muss über den lokalen Projektserver geöffnet werden.";
        console.error("East-wing prototype failed to load:", error);
    }
}

function orientedGeometry(segment, fromPortalId) {
    return segment.portals[0] === fromPortalId
        ? segment.geometry
        : [...segment.geometry].reverse();
}

function drawRoute(route, startZone, targetZone) {
    routeSegments.replaceChildren();
    routeMarkers.replaceChildren();
    floorPlan.querySelectorAll(".route-zone, .start-zone, .target-zone").forEach((zone) => {
        zone.classList.remove("route-zone", "start-zone", "target-zone");
    });

    for (const zoneId of route.zone_sequence) {
        floorPlan.querySelector(`#zone-${CSS.escape(zoneId)}`)?.classList.add("route-zone");
    }
    floorPlan.querySelector(`#zone-${CSS.escape(startZone)}`)?.classList.add("start-zone");
    floorPlan.querySelector(`#zone-${CSS.escape(targetZone)}`)?.classList.add("target-zone");

    route.segment_ids.forEach((segmentId, index) => {
        const segment = database.segments[segmentId];
        const geometry = orientedGeometry(segment, route.portal_chain[index]);
        const path = document.createElementNS(SVG_NS, "polyline");
        path.setAttribute("points", geometry.map((point) => point.join(",")).join(" "));
        path.setAttribute("class", `route-segment ${route.segment_roles[index]}`);
        path.style.animationDelay = `${index * 90}ms`;
        routeSegments.appendChild(path);
    });

    route.portal_chain.forEach((portalId, index) => {
        const portal = database.portals[portalId];
        const marker = document.createElementNS(SVG_NS, "circle");
        marker.setAttribute("cx", portal.point[0]);
        marker.setAttribute("cy", portal.point[1]);
        marker.setAttribute("r", index === 0 || index === route.portal_chain.length - 1 ? "13" : "10");
        const classes = ["route-marker"];
        if (portal.virtual) classes.push("virtual");
        if (index === route.portal_chain.length - 1) classes.push("terminal");
        marker.setAttribute("class", classes.join(" "));
        routeMarkers.appendChild(marker);
    });
}

function instruction(text, note) {
    const item = document.createElement("li");
    item.append(document.createTextNode(text));
    if (note) {
        const detail = document.createElement("span");
        detail.className = "instruction-note";
        detail.textContent = note;
        item.appendChild(detail);
    }
    return item;
}

function makeInstructions(route) {
    if (!route.portal_chain.length) {
        return [instruction(`Start und Ziel liegen in ${zoneLabel(route.zone_sequence[0])}.`, "Die Position innerhalb der Zone wird nach Regel 4.17 nicht berücksichtigt.")];
    }

    const instructions = [];
    const firstPortal = database.portals[route.portal_chain[0]];
    const firstZone = route.zone_sequence[1];
    instructions.push(instruction(
        `Verlassen Sie ${zoneLabel(route.zone_sequence[0])} durch ${firstPortal.id} in ${zoneLabel(firstZone)}.`,
        firstPortal.virtual ? "Dieses Portal ist eine virtuelle Zonengrenze, keine Tür." : "Das initiale Portal bestimmt die Abgangsrichtung."
    ));

    route.segment_ids.forEach((segmentId, index) => {
        const segment = database.segments[segmentId];
        const fromPortal = route.portal_chain[index];
        const toPortal = route.portal_chain[index + 1];
        const enteredZone = route.zone_sequence[index + 2];
        const targetReached = index === route.segment_ids.length - 1;
        const role = route.segment_roles[index];
        const verb = role === "transit" ? "Folgen Sie der Bewegungslinie" : "Durchqueren Sie die Zone";
        const text = targetReached
            ? `${verb} in ${zoneLabel(segment.zone_id)} von ${fromPortal} bis ${toPortal} und betreten Sie ${zoneLabel(enteredZone)}.`
            : `${verb} in ${zoneLabel(segment.zone_id)} von ${fromPortal} bis ${toPortal}; weiter nach ${zoneLabel(enteredZone)}.`;
        const nextPortal = database.portals[toPortal];
        const note = nextPortal.virtual
            ? `${toPortal} ist eine virtuelle Zonengrenze ohne Tür.`
            : role === "transit" ? "Transitsegment entlang der entworfenen Bewegungslinie." : "Zugangssegment am Anfang oder Ende der Route.";
        instructions.push(instruction(text, note));
    });
    return instructions;
}

function renderRouteDetails(route) {
    routeDistance.textContent = `${route.distance.toFixed(1)} SVG-Einheiten`;
    routePortalCount.textContent = String(route.portal_chain.length);
    routeCost.textContent = route.total_cost.toFixed(1);
    routeSummary.hidden = false;
    emptyState.hidden = true;
    instructionList.replaceChildren(...makeInstructions(route));
    canonicalRoute.textContent = route.sequence.join("  →  ");
    stateChain.replaceChildren(...route.state_chain.map((state) => {
        const code = document.createElement("code");
        code.textContent = `${state.zone_from} | ${state.portal_id} | ${state.zone_to}`;
        return code;
    }));
}

function renderSelectedRoute() {
    if (!database) return;
    const startZone = startSelect.value;
    const targetZone = targetSelect.value;
    const route = database.routes[startZone]?.[targetZone];
    if (!route || route.status !== "ok") {
        emptyState.hidden = false;
        emptyState.textContent = "Für dieses Zonenpaar wurde keine Route gefunden.";
        instructionList.replaceChildren();
        routeSummary.hidden = true;
        return;
    }
    drawRoute(route, startZone, targetZone);
    renderRouteDetails(route);
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    renderSelectedRoute();
});

swapButton.addEventListener("click", () => {
    const start = startSelect.value;
    startSelect.value = targetSelect.value;
    targetSelect.value = start;
    renderSelectedRoute();
});

loadPrototype();