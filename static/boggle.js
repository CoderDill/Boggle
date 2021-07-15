class BoggleGame {
  constructor(board, time) {
    this.time = time;
    this.board = $(board);
    this.guesses = new Set();
    this.score = 0;
    this.timer = setInterval(this.timeRemaining.bind(this), 1000);

    $("form.enter-guess").on("submit", this.handleSubmit.bind(this));
  }

  showGuess(guess) {
    $(".guesses").append($("<li>", { text: guess }));
  }

  showMessage(message, cls) {
    $(".message").text(message).removeClass().addClass(`message ${cls}`);
  }

  showScore() {
    $(".score").text(this.score);
  }
  async handleSubmit(evt) {
    evt.preventDefault();
    const $guess = $(".guess");
    let guess = $guess[0].value.toLowerCase();

    if (this.guesses.has(guess)) {
      this.showMessage(`${guess} has already been guessed.`, "err");
      return;
    }
    const response = await axios.get("/check-guess", {
      params: { guess: guess },
    });
    console.log(response);
    if (response.data.result === "not-word") {
      this.showMessage(`${guess} is not a valid english word`, "err");
    } else if (response.data.result === "not-on-board") {
      this.showMessage(`${guess} is not on board`, "err");
    } else {
      this.showGuess(guess);
      this.score += guess.length;
      this.showScore();
      this.guesses.add(guess);
      this.showMessage(`${guess} has been added!`, "ok");
    }
    $guess.val("");
  }

  showTimer() {
    $(".timer").text(this.time);
  }

  async timeRemaining() {
    this.time -= 1;
    this.showTimer();

    if (this.time <= 0) {
      clearInterval(this.timer);
      await this.showEndGame();
    }
  }

  async showEndGame() {
    $(".enter-guess").hide();
    const response = await axios.post("/end-game", { score: this.score });
    console.log(response);
    if (response.data.newRecord) {
      this.showMessage(`New Record! - ${this.score}`, "ok");
    } else {
      this.showMessage(`Final Score: ${this.score}`, "ok");
    }
  }
}
