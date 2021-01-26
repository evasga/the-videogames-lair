function toggleAdvancedFilters(button) {
    $('#advanced-filters').toggleClass(["collapsed"]);
    $(button).find(".fas").toggleClass("fa-rotate-180");
}

function createFilter(visibleValue, hiddenValue, name) {
    const hiddenInput = document.createElement("input");
    hiddenInput.removeAttribute("id");
    hiddenInput.type = "hidden";
    hiddenInput.name = name;
    hiddenInput.value = hiddenValue;

    const span = document.createElement("span");
    span.innerText = visibleValue;
    span.classList.add("bg-info", "text-white", "rounded-pill", "px-2", "mt-1", "mr-2", "d-inline-block");
    span.appendChild(hiddenInput);

    const close = document.createElement("button");
    close.type = "button";
    close.setAttribute("onclick", "this.parentNode.remove()")
    close.classList.add("close", "text-white", "ml-1", "line-height-inherit", "font-weight-inherit",
        "font-size-inherit");
    close.setAttribute("aria-label", "Close");
    const closeSpan = document.createElement("span");
    closeSpan.innerHTML = "&times;"
    closeSpan.setAttribute("aria-hidden", "true");
    close.appendChild(closeSpan);
    span.appendChild(close);

    return span;
}

function addFilter(originalInput, visibleValue, hiddenValue) {
    const span = createFilter(visibleValue, hiddenValue, originalInput.name);

    originalInput.parentNode.appendChild(span);
    originalInput.value = "";
}

const ageRatingOptions = document.getElementById("input-age-rating")
    .querySelectorAll("option");

function updateAgeRatings(select) {
    const system = select.value;
    const ageRatingsSelect = document.getElementById("input-age-rating");

    ageRatingsSelect.innerHTML = "";
    for (let i = 0; i < ageRatingOptions.length; i++) {
        const ageRating = ageRatingOptions[i];
        if (!(ageRating.dataset.option) || (ageRating.dataset.option === system)) {
            ageRatingsSelect.appendChild(ageRating);
        }
    }
    document.getElementById("input-age-rating").disabled = (system === "System");
}

function addAgeRatingFilter(select) {
    const ageRating = select.value;
    const systemSelect = document.getElementById("input-age-rating-system");
    const system = systemSelect.value;
    const fullAgeRating = `${system}: ${ageRating}`;

    const span = createFilter(fullAgeRating, fullAgeRating, select.name);

    const container = document.getElementById("age-rating-filters-container");
    container.appendChild(span);
}

function setYearsSlider(currentMin, currentMax) {
    const min = 1971;
    const max = 2020;

    if (!currentMin){
        currentMin = min;
    }

    if (!currentMax) {
        currentMax = max;
    }

    $(".js-range-slider").ionRangeSlider({
        type: "double",
        skin: "round",
        min: min,
        max: max,
        from: currentMin,
        to: currentMax,
        prettify: (year) => year
    });
}

function rateGame(star, gameId, rating) {
    let ratingContainer = $(star).parent();
    let oldRating = ratingContainer.find(".fas").length;
    let steamIcon = ratingContainer.find(".fa-steam");
    let wasEstimated = steamIcon.length > 0;

    /* Fill stars */
    let stars = ratingContainer.find(".fa-star");
    stars.slice(0, rating).addClass("fas").removeClass("far");
    stars.slice(rating).addClass("far").removeClass("fas");

    /* Remove Steam markers, if any */
    stars.removeClass("text-info");
    steamIcon.fadeOut();

    /* Send rating to backend */
    $.ajax({
        url: "rate-game/",
        type: "POST",
        headers: {
            "X-CSRFToken": Cookies.get("csrfcookie")
        },
        data: {
            "game_id": gameId,
            "rating": rating
        }
    }).fail( (response) => {
        /* Undo changes */
        setTimeout(() => {
            stars.slice(0, oldRating).addClass("fas").removeClass("far");
            stars.slice(oldRating).addClass("far").removeClass("fas");
            if (wasEstimated) {
                stars.addClass("text-info");
                steamIcon.fadeIn();
            }
        }, 1000);
    });
}

$(document).ready(function () {
    $("form").submit(function () {
        if (($("#advanced-filters").hasClass("collapsed"))) {
            // Don't send filters at all
            $(".advanced-search").removeAttr("name");
        } else {
            $(".advanced-search:not([type=hidden])").removeAttr("name");
            const input = document.createElement("input");
            input.name = "open";
            input.value = "true";
            input.type = "hidden";
            document.getElementById("advanced-filters").appendChild(input);
        }
    });

    $(".basic-autocomplete").autoComplete({minLength: 1, preventEnter: true});

    $(".basic-autocomplete:not(#platform-input)").on("autocomplete.select", function (event, value) {
            addFilter(this, value, value);
    });

    $("#platform-input").on("autocomplete.select", function (event, value) {
        const splitValue = value.split(" ");
        const platformAbbreviation = splitValue[0];
        let platformName = splitValue.slice(1).join(" ");
        platformName = platformName.slice(1, platformName.length-1); // Remove parenthesis

        addFilter(this, platformAbbreviation, platformName);
    });

    /* If filters were open, collapse them to make the results more visible */
    let advanced_filters = $("#advanced-filters")
    if (!advanced_filters.hasClass("collapsed")) {
        setTimeout(() => toggleAdvancedFilters($("#advanced-filters-btn")), 500);
    }
});