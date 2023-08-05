const state = {
    aspectRatio: null,
    cursorTimeout: null,
    dimensions: {
        width: null,
        height: null
    },
    objects: [],
    references: {},
    slideIdx: null,
    buildIdx: null,
    builds: [],
    go: false,
    prev: null,
    svg: null,
    control: null
};

const KEYS = {
    enter: 13,
    esc: 27,
    space: 32,
    leftArrow: 37,
    rightArrow: 39,
    b: 66,
    c: 67,
    g: 71,
    p: 80,
    x: 88,
    z: 90
}

// Set up presentation
document.addEventListener('DOMContentLoaded', () => {
    state.dimensions.width = data.size.width;
    state.dimensions.height = data.size.height;
    state.aspectRatio = data.size.width / data.size.height;

    if (window.location.search === "?control") {
        setupControlPanel();
        window.addEventListener("message", controlPanelMessageReceived);
        window.addEventListener("keydown", controlPanelKeyDownListener);
    } else if (window.location.search === "?print") {
        setupPrintout();
    } else {
        setupMainPresentation();
        window.addEventListener("keydown", mainKeyDownListener);
        window.addEventListener("resize", mainWindowResize);
        window.addEventListener("mousemove", mainWindowMouseMove);
        window.addEventListener("message", mainWindowMessageReceived);
    }
});

function setupMainPresentation() {
    const body = document.querySelector("body")
    body.style.margin = 0;
    body.style.backgroundColor = "black";

    state.svg = d3.select("body")
                  .append("svg")
                  .attr("viewBox", `0 0 ${data.size.width} ${data.size.height}`)
                  .style("background-color", "black");
    mainWindowResize();

    renderSlide(0, 0, transition=false);
    state.cursorTimeout = setTimeout(hideCursor, 1000);
}

control_state = {
    slides: [],
    selected: null
}
function setupControlPanel() {
    const body = document.querySelector("body");
    body.style.margin = 0;
    body.style.backgroundColor = "black";

    const container = d3.select("body")
                        .append("div")
                        .style("display", "flex")
                        .style("flex-wrap", "wrap")
                        .style("justify-content", "center");

    for (let i = 0; i < data.slides.length; i++) {
        const slide_container =
            container.append("div")
                     .attr("data-slide", i)
                     .style("margin", "10px")
                     .style("background-color", "#525252");
        const svg =
            slide_container.append("svg")
                           .attr("data-slide", i)
                           .attr("viewBox", `0 0 ${data.size.width} ${data.size.height}`)
                           .attr("width", 300)
                           .attr("height", 300 / (data.size.width / data.size.height))
                           .style("margin", 10);
            slide_container.append("div")
                           .attr("data-slide", i)
                           .style("font-family", "sans-serif")
                           .style("font-size", "18px")
                           .style("color", "white")
                           .style("text-align", "center")
                           .style("margin-bottom", "10px")
                           .text(i.toString() + (data.slides[i].id  ? " [" + data.slides[i].id + "]" : ""))
        control_state.slides[i] = {
            container: slide_container,
            svg: svg
        };
        slide_container.node().addEventListener("click", (e) => {
            const slide_container = e.path[e.path.length - 6];
            const slideIdx = parseInt(slide_container.dataset.slide);
            window.opener.postMessage({slideIdx: slideIdx}, "*");
        });
        renderSlidePreview(i, data.slides[i]);
    }

}

function setupPrintout() {
    const body = d3.select("body").style("margin", 0);

    for (let i = 0; i < data.slides.length; i++) {
        const div = body.append("div").attr("class", "print");
        const svg = div.append("svg")
            .attr("viewBox", `0 0 ${data.size.width} ${data.size.height}`)
            .attr("width", window.innerWidth)
            .attr("height", window.innerWidth / (data.size.width / data.size.height));
        control_state.slides[i] = {
            container: div,
            svg: svg
        }
        renderSlidePreview(i, data.slides[i]);
    }
}

// Window resizes, resize SVG to fit
function mainWindowResize() {
    let width;
    let height;
    let vpadding;
    let hpadding;
    if (window.innerWidth / state.aspectRatio <= window.innerHeight) {
        width = window.innerWidth;
        height = window.innerWidth / state.aspectRatio;
        vpadding = 1 + (window.innerHeight - height) / 2;
        hpadding = 0;
    } else {
        width = window.innerHeight * state.aspectRatio;
        height = window.innerHeight;
        vpadding = 0;
        hpadding = 1 + (window.innerWidth - width) / 2;
    }
    state.svg.attr("width", width)
             .attr("height", height)
             .style("margin-top", vpadding)
             .style("margin-bottom", vpadding)
             .style("margin-right", hpadding)
             .style("margin-left", hpadding);
}

function mainKeyDownListener(e) {
    if (state.go !== false) {
        switch (e.keyCode) {
            case KEYS.esc:
                state.go = false;
                break;
            case KEYS.enter:
                const slideNo = parseInt(state.go);
                if (isNaN(slideNo)) {
                    const slideIndex = data.slide_ids[state.go];
                    if (slideIndex !== undefined) {
                        state.prev = {slideIdx: state.slideIdx, buildIdx: state.buildIdx};
                        renderSlide(slideIndex, 0, transition=false);
                    }
                } else if (slideNo >= 0 && slideNo <= data.slides.length - 1) {
                    state.prev = {slideIdx: state.slideIdx, buildIdx: state.buildIdx};
                    renderSlide(slideNo, 0, transition=false);
                }
                state.go = false;
                break;
            default:
                state.go += String.fromCharCode(e.keyCode);
                break;
        }
        e.preventDefault();
        return;
    }
    switch (e.keyCode) {
        case KEYS.rightArrow:
        case KEYS.space:
            e.preventDefault();
            renderNext();
            break;
        case KEYS.leftArrow:
            e.preventDefault();
            renderPrevious();
            break;
        case KEYS.b: // go back to prev
            if (state.prev !== null) {
                renderSlide(state.prev.slideIdx, state.prev.buildIdx, transition=false);
                state.prev = null;
            }
            break;
        case KEYS.c: // open control panel
            if (state.control !== null) {
                state.control.close();
            }
            state.control = window.open(location.origin + location.pathname + "?control", "", "top=50,left=50,width=1100,height=600");
            setTimeout(() => {
                state.control.postMessage({slideIdx: state.slideIdx}, "*");
            }, 500);
            break;
        case KEYS.g: // go to slide
            e.preventDefault();
            state.go = "";
            break;
        case KEYS.p: // print
            window.open(location.origin + location.pathname + "?print");
            break;
        case KEYS.x:
            e.preventDefault();
            renderSlide(data.slides.length - 1, 0, transition=false);
            break;
        case KEYS.z:
            e.preventDefault();
            renderSlide(0, 0, transition=false);
            break;
        default:
            break;
    }
}

// Passes keystrokes along from control panel to main window
function controlPanelKeyDownListener(e) {
    window.opener.postMessage({keyDown: e.keyCode}, "*");
}

function mainWindowMouseMove() {
    clearTimeout(state.cursorTimeout);
    document.body.style.cursor = "";
    state.cursorTimeout = setTimeout(hideCursor, 1000);
}

function mainWindowMessageReceived(e) {
    const slideIdx = e.data.slideIdx;
    if (slideIdx !== undefined && !isNaN(slideIdx)) {
        renderSlide(slideIdx, 0, transition=false);
    }
    else if (e.data.keyDown !== undefined) {
        mainKeyDownListener({keyCode: e.data.keyDown, preventDefault: () => null});
    }
}

function controlPanelMessageReceived(e) {
    const slideIdx = e.data.slideIdx;
    if (control_state.selected !== null) {
        const old_container = control_state.slides[control_state.selected].container;
        old_container.style("background-color", "#525252");
    }
    control_state.selected = slideIdx;
    const new_container = control_state.slides[slideIdx].container;
    new_container.style("background-color", "#bbcc66");
    const node = new_container.node();
    const box = node.getBoundingClientRect();
    if (box.top < 0 || box.bottom > window.innerHeight)
        new_container.node().scrollIntoView();
}

function hideCursor() {
    document.body.style.cursor = "none";
}

function renderNext() {
    if (state.buildIdx === state.builds.length) {
        renderSlide(Math.min(state.slideIdx + 1, data.slides.length - 1), 0, transition=true);
    } else {
        // Render next build
        state.builds[state.buildIdx].forEach(obj => {
            obj.attr("display", "");
        });
        state.buildIdx += 1;
    }
}

function renderPrevious() {
    if (state.buildIdx === 0) {
        renderSlide(Math.max(state.slideIdx - 1, 0), 0, transition=false);
    } else {
        // Render previous build
        state.buildIdx -= 1;
        state.builds[state.buildIdx].forEach(obj => {
            obj.attr("display", "none");
        });
    }
}

function renderSlide(slideIdx, buildIdx, transition) {

    // Update slide index
    state.slideIdx = slideIdx;
    state.buildIdx = 0;
    state.builds = [];
    const slide = data.slides[slideIdx];

    // Notify control panel if it exists
    if (state.control !== null) {
        state.control.postMessage({slideIdx: slideIdx}, "*");
    }

    // If no transition, then don't need previous references
    if (transition === false) {
        state.references = {};
    }

    // Get references in new slide present at start of slide
    const references =
        new Set(slide.objects
                     .filter(obj => obj.id !== undefined &&
                            (obj.build === false || obj.build === undefined))
                     .map(obj => obj.id));

    // Get objects that need to make a transition
    const transitioners =
        Object.keys(state.references)
        .filter(id => references.has(id))
        .reduce((obj, key) => {
            obj[key] = state.references[key];
            return obj;
        }, {});

    // Remove previous content
    for (let i = 0; i < state.objects.length; i++) {
        if (transition === false ||
            Object.values(transitioners).some((k) =>
                (k.object == state.objects[i])) === false) {
            state.objects[i].remove();
            delete state.objects[i];
        }
    }
    state.objects = state.objects.filter(obj => obj !== undefined);

    // Update with current slide
    state.svg.style("background-color", slide.backgroundColor);
    switch (slide.layout) {
        case "bullets":
            renderBulletsSlide(slide);
            break;
        case "html":
            renderHTMLSlide(slide);
            break;
        case "section":
            renderSectionSlide(slide);
            break;
        case "title":
            renderTitleSlide(slide);
            break;
    }

    // Add objects
    renderObjects(slide, transitioners);

    // Filter out undefined builds
    state.builds = state.builds.filter(build => build !== undefined);

    // Render builds as needed (e.g. if returning back to slide)
    for (let i = 0; i < buildIdx; i++) {
        state.builds[i].forEach(obj => {
            obj.attr("display", "");
        });
    }
    state.buildIdx = buildIdx;
}

function renderSlidePreview(i, slide) {
    const previewSvg = control_state.slides[i].svg;
    previewSvg.style("background-color", slide.backgroundColor);
    switch (slide.layout) {
        case "bullets":
            renderBulletsSlide(slide, svg=previewSvg, build=false);
            break;
        case "html":
            renderHTMLSlide(slide, svg=previewSvg, build=false);
            break;
        case "section":
            renderSectionSlide(slide, svg=previewSvg, build=false);
            break;
        case "title":
            renderTitleSlide(slide, svg=previewSvg, build=false);
            break;
    }
    renderObjects(slide, {}, svg=previewSvg, build=false);
}

function renderBulletsSlide(slide, svg=null, build=true) {
    const heading =
        (svg || state.svg).append("text")
             .attr("x", slide.title.padding_left)
             .attr("y", slide.title.padding_top + slide.title.size)
             .attr("font-size", slide.title.size)
             .attr("font-family", slide.title.font)
             .attr("fill", slide.title.color)
             .text(slide.title.content);
    state.objects.push(heading);

    const bullets_height = state.dimensions.height
                          - slide.title.padding_top * 3
                          - slide.title.size;
    const bullet_height = slide.bullets.size + slide.bullets.spacing;
    const bullet_y = slide.title.padding_top
                     + slide.title.size + (bullets_height / 2)
                     - bullet_height * (slide.bullets.content.length / 2);
    const bullets =
        (svg || state.svg).append("text")
             .attr("x", slide.bullets.padding_left)
             .attr("y", bullet_y)
             .attr("dominant-baseline", "middle")
             .attr("font-size", slide.bullets.size)
             .attr("font-family", slide.bullets.font)
             .style("fill", slide.bullets.color);
    for (let i = 0; i < slide.bullets.content.length; i++) {
        const bullet =
            bullets.append("tspan")
                   .attr("x", slide.bullets.padding_left + ((slide.bullets.content[i] || {}).spacing || 0))
                   .attr("dy", i > 0 ? slide.bullets.size + slide.bullets.spacing : 0)
                   .attr("display", (build && slide.bullets.build) ? "none" : "")
                   .style("fill", (slide.bullets.content[i] || {}).color || slide.bullets.color)
                   .text(slide.bullets.bullet + ((slide.bullets.content[i] || {}).text || " "));
        if (slide.bullets.build) {
            state.builds.push([bullet]);
        }
    }
    state.objects.push(bullets);
}

function renderHTMLSlide(slide, svg=null, build=true) {
    const html =
        (svg || state.svg).append("foreignObject")
                 .attr("x", 0)
                 .attr("y", 0)
                 .attr("width", "100%")
                 .attr("height", "100%");
    html.append("xhtml:div")
        .attr("xmlns", "http://www.w3.org/2000/svg")
        .style("background-color", slide.backgroundColor)
        .style("zoom", "220%")
        .style("margin", 0)
        .style("position", "absolute")
        .style("height", "100%")
        .style("width", "100%")
        .html(slide.content || "");
    state.objects.push(html);
}

function renderSectionSlide(slide, svg=null, build=true) {
    const section =
        (svg || state.svg).append("text")
             .attr("x", "50%")
             .attr("y", "50%")
             .attr("dominant-baseline", "middle")
             .attr("text-anchor", "middle")
             .attr("font-size", slide.size)
             .attr("font-family", slide.font)
             .style("fill", slide.color)
             .text(slide.content);
    state.objects.push(section);
}

function renderTitleSlide(slide, svg=null, build=true) {
    const title =
        (svg || state.svg).append("text")
             .attr("x", "50%")
             .attr("y", "45%")
             .attr("dominant-baseline", "middle")
             .attr("text-anchor", "middle")
             .attr("font-size", slide.title.size)
             .attr("font-family", slide.title.font)
             .style("fill", slide.title.color)
             .text(slide.title.content);
    state.objects.push(title);

    const subtitle =
        (svg || state.svg).append("text")
             .attr("x", "50%")
             .attr("y", "60%")
             .attr("dominant-baseline", "middle")
             .attr("text-anchor", "middle")
             .attr("font-size", slide.subtitle.size)
             .attr("font-family", slide.subtitle.font)
             .style("fill", slide.subtitle.color);
    for (let i = 0; i < slide.subtitle.content.length; i++) {
        subtitle.append("tspan")
                .attr("x", "50%")
                .attr("dy", i > 0 ? slide.subtitle.size + 5 : 0)
                .text(slide.subtitle.content[i]);
    }
    state.objects.push(subtitle);
}

function transitionCall(transition, attrs, style) {

    for (let key in attrs)
        transition.attr(key, attrs[key]);
    for (let key in style)
        transition.style(key, style[key]);
}

function renderObjects(slide, transitioners, svg=null, build=true) {

    state.references = {};
    for (let i = 0; i < slide.objects.length; i++) {
        const object = slide.objects[i];

        // Check if object has id, should be transitioned, and isn't a later build
        if (object.id !== undefined
            && transitioners[object.id] !== undefined
            && build
            && (object.build === undefined || object.build === false)) {

            // Transition object from previous slide
            const obj = transitioners[object.id].object;
            const transition =
                d3.transition()
                  .duration(transitioners[object.id].transition_length)
                  .ease(d3.easeLinear);
            obj.transition(transition).call(transitionCall, object.attrs, object.style);

            // Record reference to object
            state.references[object.id] = {
                object: obj,
                transition_length: object.transition_length
            };
        } else {
            renderObject(object, (svg || state.svg), build, true);
        }
    }
}

function renderObject(object, parent_object, build, add_to_references) {
    let obj = null;

    if (object.type == "group") {
        obj = parent_object.append("g")
                           .attr("transform", object.attrs.transform);
        for (let i = 0; i < object.children.length; i++) {
            renderObject(object.children[i], obj, build, false);
        }
    }
    else if (object.type === "html") {

        // Create HTML object
        obj =
            parent_object.append("foreignObject")
                         .attr("x", object.attrs.x)
                         .attr("y", object.attrs.y)
                         .attr("height", object.attrs.height)
                         .attr("width", object.attrs.width);
        obj.append("xhtml:div")
           .attr("xmlns", "http://www.w3.org/2000/svg")
           .style("background-color", object.style.fill)
           .style("zoom", object.style.zoom)
           .style("margin", 0)
           .style("position", "absolute")
           .style("height", "100%")
           .style("width", "100%")
           .html(object.content || "");

    } else {

        // Create non-HTML object
        obj = parent_object.append(object.type);
        for (let key in object.attrs) {
            obj.attr(key, object.attrs[key]);
        }
        for (let key in object.style) {
            obj.style(key, object.style[key]);
        }
        if (object.text !== undefined) {
            for (let i = 0; i < object.text.length; i++) {
                const tspan = obj.append("tspan")
                   .attr("x", object.attrs.x)
                   .attr("dy", i > 0 ? parseInt(object.attrs["font-size"]) + object.attrs.spacing : 0);
                if (object.html === true)
                    tspan.html(object.text[i]);
                else
                    tspan.text(object.text[i]);
            }
        }
    }

    // Check if object should be built later
    if (build && object.build) {
        obj.attr("display", "none");
        if (object.build === true) {
            state.builds.push([obj]);
        } else if (state.builds[object.build] === undefined) {
            state.builds[object.build] = [obj];
        } else {
            state.builds[object.build].push(obj);
        }
    }

    // Add top-level objects to references and objects, but not members of groups
    if (add_to_references) {
        // Record reference to object if identified
        if (object.id !== undefined) {
            state.references[object.id] = {
                object: obj,
                transition_length: object.transition_length
            };
        }
        state.objects.push(obj);
    }
}
