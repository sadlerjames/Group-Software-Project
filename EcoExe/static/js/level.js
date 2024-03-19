export default class Level {
    constructor(wastageTypes, difficulty) {
        this.#matchings = {};
		this.#completedMatchings = [];

        for(let wastage of Object.values(wastageTypes)) {
            //this.#matchings[emoji.emojiID] = new Matching(emoji, 2);
			this.#matchings[wastage[0].alt] = wastage;
        }
        this.#flippedCards = new Array();
        this.#setDifficulty(difficulty);
    }

    get flippedCards() {
        return this.#flippedCards;
    }
    appendCard(card) {
        this.#flippedCards.push(card);
    }
    resetFlipped() {
        this.#flippedCards.length = 0;
    }

    get matchings() {
        return this.#matchings;
    }

    static get resetting() {
        return Level.#resetting;
    }
    static set resetting(resetState) {
        if(typeof(resetState) === "boolean")
            Level.#resetting = resetState;
    }

    get details() {
        return {
            levelscore: this.score,
            levelmistakes: this.mistakes
        }
    }

    isLevelComplete() {
        for(let matching of Object.values(this.#matchings))
            if(matching)
                return false;
        return true;
    }
	
	completeMatching(type) {
		this.#completedMatchings.push(type);
		this.#matchings[type] = false;
	}

    get score() {
        switch(Level.#difficulty) {
            case "simple":
                return this.#score; 
            case "medium":
                return this.#score;
            case "complex":
                console.log(this.#score);
                return this.#score;
        }
    }
    addScore() {
        this.#score += (500 / (this.#mistakes > 0 ? this.#mistakes : 1));
    }

    get mistakes() {
        return this.#mistakes;
    }
    addMistake() {
        this.#mistakes++;
    }

    static get difficulty() {
        return (Level.#difficulty) ? Level.#difficulty : undefined;
    }

    #setDifficulty(difficulty) {
        switch(difficulty) {
            case "simple":
                Level.#difficulty = difficulty;
                break;
            case "medium":
                Level.#difficulty = difficulty;
                break;
            case "complex":
                Level.#difficulty = difficulty;
                break;
        }
    }

    #matchings;
	#completedMatchings;
    #flippedCards;
    #score = 0;
    #mistakes = 0;
    #highScore;
    static #difficulty;
    static #resetting = false;
}

class Matching {
    constructor(emoji, cardCount) {
        this.#emoji = emoji;
        this.#cardCount = cardCount;
        this.#originalCount = this.#cardCount;
        this.#isComplete = false;
    }

    get emoji() {
        return this.#emoji;
    }

    get cardCount() {
        return this.#cardCount;
    }
    addCard() {
        if(this.#cardCount < 4) {
            ++this.#cardCount;
            ++this.#originalCount;
        } 
    }
    decrementCount() {
        --this.#cardCount;
    }
    resetCount() {
        this.#cardCount = this.#originalCount;
    }
    updateCount(previousLevelMatching) {
        this.#cardCount = previousLevelMatching.cardCount;
        this.#originalCount = previousLevelMatching.#originalCount;
    }

    get completed() {
        return this.#isComplete;
    }
    completeMatching() {
        this.#isComplete = true;
    }
    
    #emoji;
    #cardCount;
    #originalCount;
    #isComplete;
}