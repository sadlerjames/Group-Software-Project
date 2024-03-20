export default class Level {
    constructor(wastageTypes) {
        this.#matchings = {};
		this.#completedMatchings = [];

        for(let wastage of Object.values(wastageTypes))
			this.#matchings[wastage[0].alt] = wastage;

        this.#flippedCards = new Array();
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
		return this.#score;
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


    #matchings;
	#completedMatchings;
    #flippedCards;
    #score = 0;
    #mistakes = 0;
    #highScore;
    //static #difficulty;
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