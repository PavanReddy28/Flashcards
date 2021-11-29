const fields = 10

const addCardField = (e) => {
    var count = parseInt(document.getElementById("cards_num").value)-1
    console.log(x)
    var cards = document.getElementById("cardFields")
    var x = 1
    while (x<=count && x<=fields-1) {
        x++;
        cards.innerHTML +=
            `
            <div class="card" style="padding:1rem; margin: 1rem;">
            <p class="lead">Card ${x}</p>
            <div class="col ">
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="front_card_${x}" name="front_${x}" placeholder="Front Card">
                    <label for="front_card_${x}">Front Card</label>
                </div>
                <div class="form-floating mb-3">
                    <input type="text" class="form-control" id="back_card_${x}" name="back_${x}" placeholder="Back Card">
                    <label for="back_card_${x}">Back Card</label>
                </div>
            </div>
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="lang_card_${x}" name="lang_${x}" placeholder="Language Front">
                <label for="lang_${x}">Language Front</label>
            </div>
            <div class="form-floating mb-3">
                <input type="text" class="form-control" id="lang2_card_${x}" name="lang2_${x}" placeholder="Language Back">
                <label for="lang2_${x}">Language Back</label>
            </div>
            <div class="mb-3">
                <label for="difficulty${x}">Choose Difficulty</label>
                <select class="form-select" aria-label="Default select example" id="difficulty_${x}" name="diff_${x}">
                    <option value="1" selected>Easy</option>
                    <option value="2">Moderate</option>
                    <option value="3">Difficult</option>
                    </select>
            </div>
        </div>
            `;
    }
}


const onDeckForm = (e) => {
    e.preventDefault();


}