const GRAPH_URL = "eg-routing-graph.json";
const ROUTES_URL = "eg-routes.json";
const SVG_URL = "assets/bfw-eg.svg";
const SVG_NS = "http://www.w3.org/2000/svg";

const form = document.querySelector("#route-form");
const startSelect = document.querySelector("#start-zone");
const targetSelect = document.querySelector("#target-zone");
const swapButton = document.querySelector("#swap-zones");
const startEntranceButton = document.querySelector("#start-entrance");
const targetEntranceButton = document.querySelector("#target-entrance");
const mapPickOptions = document.querySelectorAll('input[name="map-pick-endpoint"]');
const modelStatus = document.querySelector("#model-status");
const floorPlan = document.querySelector("#floor-plan");
const mapUnavailable = document.querySelector("#map-unavailable");
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

let graph = null;
let routeTable = null;
let mapPickEndpoint = "start";

function populateSelect(select, zoneIds) {
    const fragment = document.createDocumentFragment();
    for (const zoneId of zoneIds) {
        const option = document.createElement("option");
        option.value = zoneId;
        option.textContent = zoneId === "exterior" ? "Haupteingang" : zoneId;
        fragment.appendChild(option);
    }
    select.replaceChildren(fragment);
}

function segmentFor(zoneId, portalA, portalB) {
    const pair = new Set([portalA, portalB]);
    return (graph.segments[zoneId] ?? []).find(
        (segment) => pair.size === 2 && pair.has(segment.portals[0]) && pair.has(segment.portals[1])
    );
}

function zonesForPortal(portalId) {
    const zones = portalId.split("_");
    if (zones.length === 3 && /^\d+$/.test(zones[2])) zones.pop();
    if (zones.length !== 2 || zones.some((zoneId) => !graph.zones[zoneId])) {
        throw new Error(`Portal-ID ist keinem Zonenpaar zuzuordnen: ${portalId}`);
    }
    return zones;
}

function setEndpoint(role, zoneId) {
    if (!routeTable?.zones.includes(zoneId)) return;
    (role === "start" ? startSelect : targetSelect).value = zoneId;
    renderSelectedRoute();
}

function configureMapZones() {
    const selectableZoneIds = new Set(routeTable.zones);
    for (const zoneElement of floorPlan.querySelectorAll('[id^="zone-"]')) {
        const zoneId = zoneElement.id.slice("zone-".length);
        zoneElement.dataset.routeZone = zoneId;
        zoneElement.classList.add(
            selectableZoneIds.has(zoneId) ? "map-zone-selectable" : "map-zone-passive"
        );
    }
}

function buildRoute(startZone, targetZone) {
    const startIndex = routeTable.zones.indexOf(startZone);
    const targetIndex = routeTable.zones.indexOf(targetZone);
    const portalIndexes = routeTable.routes[startIndex]?.[targetIndex];
    if (portalIndexes === null || portalIndexes === undefined) return null;

    const portalChain = portalIndexes.map((index) => routeTable.portals[index]);
    const zoneSequence = [startZone];
    for (const portalId of portalChain) {
        const connectedZones = graph.portals[portalId]?.zones ?? zonesForPortal(portalId);
        if (!connectedZones?.includes(zoneSequence.at(-1))) {
            throw new Error(`Portalfolge ist im Modell nicht zusammenhängend: ${portalId}`);
        }
        zoneSequence.push(connectedZones.find((zoneId) => zoneId !== zoneSequence.at(-1)));
    }

    const segments = [];
    for (let index = 0; index < portalChain.length - 1; index += 1) {
        const zoneId = zoneSequence[index + 1];
        const segment = segmentFor(zoneId, portalChain[index], portalChain[index + 1]);
        if (!segment) throw new Error(`Routensegment fehlt in Zone ${zoneId}`);
        segments.push({ ...segment, zone_id: zoneId });
    }

    const states = portalChain.map((portalId, index) => ({
        zone_from: zoneSequence[index],
        portal_id: portalId,
        zone_to: zoneSequence[index + 1],
    }));
    const distance = segments.reduce((total, segment) => total + segment.distance_m, 0);
    const stateCost = states.reduce(
        (total, state) => total + Number(graph.state_costs?.[`${state.zone_from}|${state.portal_id}|${state.zone_to}`] ?? 0),
        0
    );
    const segmentCost = segments.reduce((total, segment, index) => {
        const key = `${portalChain[index]}|${segment.zone_id}|${portalChain[index + 1]}`;
        return total + Number(graph.segment_costs?.[key] ?? 0);
    }, 0);

    return {
        portal_chain: portalChain,
        zone_sequence: zoneSequence,
        state_chain: states,
        segments,
        distance,
        total_cost: distance + stateCost + segmentCost,
    };
}

function orientSegment(segment, fromPortalId) {
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

    route.segments.forEach((segment, index) => {
        const geometry = orientSegment(segment, route.portal_chain[index]);
        const path = document.createElementNS(SVG_NS, "polyline");
        path.setAttribute("points", geometry.map((point) => point.join(",")).join(" "));
        const role = index === 0 || index === route.segments.length - 1 ? "access" : "transit";
        path.setAttribute("class", `route-segment ${role}`);
        path.style.animationDelay = `${index * 70}ms`;
        routeSegments.appendChild(path);
    });

    route.portal_chain.forEach((portalId, index) => {
        const portal = graph.portals[portalId];
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

function makeInstructions(route) {
    if (!route.portal_chain.length) {
        const item = document.createElement("li");
        item.textContent = route.zone_sequence[0] === "exterior"
            ? "Start und Ziel liegen am Haupteingang."
            : `Start und Ziel liegen in ${route.zone_sequence[0]}.`;
        return [item];
    }

    if (
        route.segments.length === 0
        && route.zone_sequence.at(-1) === "exterior"
        && graph.portals[route.portal_chain.at(-1)]?.main_entrance
    ) {
        const item = document.createElement("li");
        item.textContent = `Verlassen Sie ${route.zone_sequence[0]} durch den Haupteingang.`;
        return [item];
    }

    const instructions = [];
    const firstPortal = route.portal_chain[0];
    const startsAtMainEntrance = route.zone_sequence[0] === "exterior"
        && graph.portals[firstPortal]?.main_entrance;
    instructions.push(startsAtMainEntrance
        ? `Betreten Sie ${route.zone_sequence[1]} durch den Haupteingang.`
        : `Verlassen Sie ${route.zone_sequence[0]} durch ${firstPortal} in ${route.zone_sequence[1]}.`);
    route.segments.forEach((segment, index) => {
        const fromPortal = route.portal_chain[index];
        const toPortal = route.portal_chain[index + 1];
        const nextZone = route.zone_sequence[index + 2];
        const reachesMainEntrance = nextZone === "exterior"
            && graph.portals[toPortal]?.main_entrance;
        const text = reachesMainEntrance
            ? `Gehen Sie in ${segment.zone_id} von ${fromPortal} bis zum Haupteingang.`
            : index === route.segments.length - 1
                ? `Durchqueren Sie ${segment.zone_id} von ${fromPortal} bis ${toPortal} und betreten Sie ${nextZone}.`
                : `Durchqueren Sie ${segment.zone_id} von ${fromPortal} bis ${toPortal}; weiter nach ${nextZone}.`;
        instructions.push(text);
    });
    return instructions.map((text) => {
        const item = document.createElement("li");
        item.textContent = text;
        return item;
    });
}

function clearRoute() {
    routeSegments.replaceChildren();
    routeMarkers.replaceChildren();
    floorPlan.querySelectorAll(".route-zone, .start-zone, .target-zone").forEach((zone) => {
        zone.classList.remove("route-zone", "start-zone", "target-zone");
    });
}

function renderSelectedRoute() {
    if (!graph || !routeTable) return;
    const startZone = startSelect.value;
    const targetZone = targetSelect.value;
    const route = buildRoute(startZone, targetZone);
    if (!route) {
        clearRoute();
        routeSummary.hidden = true;
        instructionList.replaceChildren();
        canonicalRoute.textContent = "";
        stateChain.replaceChildren();
        emptyState.hidden = false;
        emptyState.textContent = "Für dieses Zonenpaar wurde keine Route gefunden.";
        return;
    }

    if (floorPlan.firstElementChild) drawRoute(route, startZone, targetZone);
    routeDistance.textContent = `${route.distance.toFixed(1)} m`;
    routePortalCount.textContent = String(route.portal_chain.length);
    routeCost.textContent = route.total_cost.toFixed(1);
    routeSummary.hidden = false;
    emptyState.hidden = true;
    instructionList.replaceChildren(...makeInstructions(route));
    canonicalRoute.textContent = route.zone_sequence.flatMap((zoneId, index) =>
        index < route.portal_chain.length ? [zoneId, route.portal_chain[index]] : [zoneId]
    ).join("  →  ");
    stateChain.replaceChildren(...route.state_chain.map((state) => {
        const code = document.createElement("code");
        code.textContent = `${state.zone_from} | ${state.portal_id} | ${state.zone_to}`;
        return code;
    }));
}

async function loadPrototype() {
    try {
        const [graphResponse, routesResponse] = await Promise.all([
            fetch(GRAPH_URL, { cache: "no-cache" }),
            fetch(ROUTES_URL, { cache: "no-cache" }),
        ]);
        if (!graphResponse.ok || !routesResponse.ok) {
            throw new Error(`Routendaten: ${graphResponse.status}, ${routesResponse.status}`);
        }
        [graph, routeTable] = await Promise.all([graphResponse.json(), routesResponse.json()]);
        if (routeTable.format !== "wegweiser-route-table") {
            throw new Error("Unbekanntes Routenformat");
        }

        populateSelect(startSelect, routeTable.zones);
        populateSelect(targetSelect, routeTable.zones);
        startSelect.value = routeTable.zones.includes("E.01") ? "E.01" : routeTable.zones[0];
        targetSelect.value = routeTable.zones.includes("E.52") ? "E.52" : routeTable.zones.at(-1);
        const mainEntrances = routeTable.portals.filter(
            (portalId) => graph.portals[portalId]?.main_entrance
                && zonesForPortal(portalId).includes("exterior")
        );
        const entranceAvailable = routeTable.zones.includes("exterior") && mainEntrances.length === 1;
        startEntranceButton.disabled = !entranceAvailable;
        targetEntranceButton.disabled = !entranceAvailable;
        const pairCount = routeTable.zones.length ** 2;
        modelStatus.textContent = `${routeTable.zones.length} Zonen · ${routeTable.portals.length} Portale · ${pairCount.toLocaleString("de-DE")} Routen · ${routeTable.provenance}`;
        if (routeTable.provenance !== "verified") modelStatus.dataset.unverified = "true";

        const svgResponse = await fetch(SVG_URL, { cache: "no-cache" });
        if (svgResponse.ok) {
            floorPlan.innerHTML = await svgResponse.text();
            configureMapZones();
            mapUnavailable.hidden = true;
        }
        renderSelectedRoute();
    } catch (error) {
        modelStatus.textContent = "Routendaten konnten nicht geladen werden";
        modelStatus.dataset.error = "true";
        emptyState.textContent = "Die Routendaten sind nicht verfügbar. Die Seite muss über GitHub Pages oder einen lokalen Webserver geöffnet werden.";
        console.error("EG prototype failed to load:", error);
    }
}

form.addEventListener("submit", (event) => {
    event.preventDefault();
    renderSelectedRoute();
});

startSelect.addEventListener("change", renderSelectedRoute);
targetSelect.addEventListener("change", renderSelectedRoute);

for (const option of mapPickOptions) {
    option.addEventListener("change", () => {
        if (!option.checked) return;
        mapPickEndpoint = option.value;
        for (const label of document.querySelectorAll(".map-pick-mode label")) {
            label.classList.toggle("is-selected", label.contains(option));
        }
    });
}

floorPlan.addEventListener("click", (event) => {
    const zoneElement = event.target.closest?.("[data-route-zone]");
    if (!zoneElement || !routeTable.zones.includes(zoneElement.dataset.routeZone)) return;
    setEndpoint(mapPickEndpoint, zoneElement.dataset.routeZone);
});

startEntranceButton.addEventListener("click", () => setEndpoint("start", "exterior"));
targetEntranceButton.addEventListener("click", () => setEndpoint("target", "exterior"));

swapButton.addEventListener("click", () => {
    const start = startSelect.value;
    startSelect.value = targetSelect.value;
    targetSelect.value = start;
    renderSelectedRoute();
});

loadPrototype();