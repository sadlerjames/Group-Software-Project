import Level from "./level.js";
//import Emoji from "./modules/emoji.js";

"use strict";

function startGame() {
    const game = new Game(false);
    const divPairs = document.getElementById("divPairs");
    const tblPairs = document.createElement("table");
    tblPairs.id = "tblPairs";
    
    document.getElementById("btnStartGame").remove();
    
    divPairs.append(tblPairs);
    game.loadNextLevel();
}

function showCard(card) {
	if(card !== "undefined") {
		for(let feature of card.querySelectorAll(".skin,.mouth,.eyes"))
			feature.hidden = false;
		card.querySelector(".hidden").hidden = true;
	}
}

function hideCard(card) {
	if(card !== "undefined") {
		for(let feature of card.querySelectorAll(".skin,.mouth,.eyes"))
			feature.hidden = true;
		card.querySelector(".hidden").hidden = false;
	}
}

function flipCard(card, currentLevel) {
    if(Level.resetting || card.dataset.isFlipped === "true") return;

    currentLevel.flippedCards.push(card);
	//console.log(currentLevel.flippedCards[0]);
    // check if card is the same type as those already in flipped cards
    if(card.dataset.type === currentLevel.flippedCards[0].dataset.type) {
        card.dataset.isFlipped = true;

		showCard(card);
		//console.log(currentLevel.matchings);
        if(currentLevel.flippedCards.length == currentLevel.matchings[card.dataset.type]) {
            for(let flippedCard of currentLevel.flippedCards)
                flippedCard.style.backgroundColor = 'gold';
            currentLevel.addScore();
            currentLevel.completeMatching(card.dataset.type);
            currentLevel.resetFlipped(); // empties currentLevel.flippedCards
        }
    } else {
        // selected card does not follow current matching
        showCard(card);
        currentLevel.addMistake();
        for(let flippedCard of currentLevel.flippedCards)
            flippedCard.style.backgroundColor = "red";
        resetCards(currentLevel);
    }
}

function chooseWastage(matches) {
	const keys = Object.keys(matches);
	
	var wastage;
    do {
        wastage = keys[Math.floor(Math.random() * keys.length)];
    } while(matches[wastage].length == 0);
	
	// picks random image
	const random = Math.floor(Math.random() * matches[wastage].length);
	const chosenWastage = matches[wastage][random];
	matches[wastage].splice(random,1);
    
    return chosenWastage;
}

async function resetCards(currentLevel) {
    Level.resetting = true;
    // wait 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));

    // reset flipped cards
    for(let flippedCard of currentLevel.flippedCards) {
        hideCard(flippedCard);
        flippedCard.style.backgroundColor = "grey";
        flippedCard.dataset.isFlipped = false;
    }
    currentLevel.resetFlipped();
    Level.resetting = false;
}

function getShape(matches) {
    let totalCount = Object.values(matches).map(
        (matching) => matching.length).reduce((x,y) => x + y);
    let shapes = {};
    for(let i = 2; i <= totalCount / 2; i++) {
        let result = totalCount / i;
        if(Number.isInteger(result))
            shapes[i] = result;
    }
    let shapeKey = Object.keys(shapes)[Math.ceil(Object.keys(shapes).length/2)-1];
    return [shapeKey, shapes[shapeKey]];
}

class Game {
	static #hiddenEmoji;
	static #hide; 
	#wastageTypes = {
		rubbish: ['toilet-roll','plastic-bag','blue-roll'],
		recycle: ['cardboard','plastic-bottle','paper'],
		food: ['banana','meat','eggplant']
	};
	#completedMatchings;
	#currentLevel;

    constructor() {
		let level1, level2, level3;
		let matchings1,matchings2,matchings3;
		let rubbishImage, recycleImage, foodImage;
		
		this.#currentLevel = 0;
		this.#completedMatchings = new Array();
		
		rubbishImage = new Image();
		rubbishImage.src = './pairs-assets/trash-rubbish.png';
		rubbishImage.alt = 'rubbish';
		rubbishImage.dataset.type = 'rubbish';
		rubbishImage.hidden = false;
		
		recycleImage = new Image();
		recycleImage.src = './pairs-assets/trash-recycle.png';
		recycleImage.alt = 'recycle';
		recycleImage.dataset.type = 'recycle';
		recycleImage.hidden = false;
		
		foodImage = new Image();
		foodImage.src = './pairs-assets/trash-food.png';
		foodImage.alt = 'food';
		foodImage.dataset.type = 'food';
		foodImage.hidden = false;
		
		// select 2 random from rubbish and recycle here
		
		let rubbishSelection = [rubbishImage,this.#randomWastage('rubbish'),this.#randomWastage('rubbish')];
		let recycleSelection = [recycleImage, this.#randomWastage('recycle'),this.#randomWastage('recycle')];
		
		matchings1 = {
			'rubbish': [...rubbishSelection],
			'recycle': [...recycleSelection]
		};
		
		matchings2 = {
			'rubbish': [...rubbishSelection],
			'recycle': [...recycleSelection]
		};
		
		// add food selection here
		let foodSelection = [foodImage, this.#randomWastage('food'),this.#randomWastage('food')];
		matchings2.food = foodSelection;
		
		matchings3 = {
			'rubbish': [...rubbishSelection],
			'recycle': [...recycleSelection],
			'food': [...foodSelection]
		};
		
		// appends last item in arrays
	
		
		matchings3['rubbish'].push(this.#randomWastage('rubbish'));
		matchings3['recycle'].push(this.#randomWastage('recycle'));
		matchings3['food'].push(this.#randomWastage('food'));
	
		level1 = new Level(matchings1,'complex');
		level2 = new Level(matchings2,'complex');
		level3 = new Level(matchings3,'complex');
		
		
        // creates 3 random emojis
        //for(let i = 0; i < 3; i++)
        //    emojis.push(this.#randomEmoji(emojis));
        // this.#hideEmojis = hideEmojis;
        this.#levels = [level1, level2, level3];
    }

    get totalScore() {
        console.log(this.#levels);
		
		this.#levels.forEach(level => console.log(level));
		console.log(this.#levels.map((
			level => level.score
		)));
        return this.#levels.map(
            (level) => level.score).reduce(
                (accScore, currentScore) => accScore + currentScore
            );
    }

    get totalMistakes() {
        //console.log(this.#levels.map((level) => level.mistakes));
        return this.#levels.map(
            (level) => level.mistakes).reduce(
                (accMistakes, currentMistakeCount) => accMistakes + currentMistakeCount  
            );
    }

    get gameData() {
        return "test";
    }

    get levels() {
        return this.#levels;
    }

    generateNextLevel() {
        let nextEmojiSet = Object.values(this.currentLevel.matchings).map(
            (matching) => matching.emoji);
            
        nextEmojiSet.push(this.#randomEmoji(nextEmojiSet));
        let nextLevel = new Level(nextEmojiSet, "complex");
        
        Object.keys(this.currentLevel.matchings).forEach(
            (matching) => nextLevel.matchings[matching].updateCount(
                this.currentLevel.matchings[matching]));

        let arrangedMatchings = {
            "2": Object.values(nextLevel.matchings).filter((matching) => matching.cardCount === 2),
            "3": Object.values(nextLevel.matchings).filter((matching) => matching.cardCount === 3),
            "4": Object.values(nextLevel.matchings).filter((matching) => matching.cardCount === 4)
        }
        
        let matchingToIncrement;
        // every 3rd level a 3-combination is upgraded to a 4-combination
        if(this.#levels.length % 3 === 0) {
            matchingToIncrement = arrangedMatchings[3].shift();
            matchingToIncrement.addCard();
        } else { // otherwise a 2-combination is upgraded to a 3-combination
            matchingToIncrement = arrangedMatchings[2].shift();
            matchingToIncrement.addCard();
        }

        this.#levels.push(nextLevel);
    }

    loadNextLevel() {
		let level = this.#levels[this.#currentLevel];
		//console.log(level);
        let tblPairs = document.getElementById("tblPairs");
        let shape = getShape(level.matchings);
        let typeCount = level.matchings['rubbish'].length;
		
        // clear table for upcoming level
        Object.values(tblPairs.getElementsByTagName("tr")).forEach(
            (child) => child.remove());
		
		
        // generate table
        for(let i = 0; i < shape[0]; i++) {
            const row = tblPairs.insertRow();
            for(let j = 0; j < shape[1]; j++) {
                const cell = row.insertCell();
                const card = document.createElement("div");
                const wastage = chooseWastage(level.matchings);
                //console.log(wastage);
                card.className = 'card';
                card.dataset.isFlipped = false;
				card.dataset.type = wastage.dataset.type;
				
                card.onclick = () => {
                    flipCard(card, level);
                    if(level.isLevelComplete()) {
						console.log(this.#isGameComplete);
                        if(this.#isGameComplete) {
                            // console.log("DONE!");
                            tblPairs.hidden = true;
                            frmFinish = document.getElementById("frmFinish");
                            frmFinish.hidden = false;
							console.log(this.#json);
                            frmFinish.querySelector('input[name="score"]').value = this.#json;
                        } else {
                            //this.generateNextLevel();
							console.log(this.#currentLevel);
                            this.loadNextLevel();
                        }
                    }
                }
                //wastage.addToCard(card);
				if(card !== "undefined" && wastage !== 'undefined') {
					card.append(wastage.cloneNode(true));
					card.append(Game.#hiddenEmoji.cloneNode(true));
				}
                cell.appendChild(card);
            }
        }

		for(let type of Object.keys(level.matchings)) {
			level.matchings[type] = typeCount;
		}
		//Object.values(level.matchings).map(x => x = typeCount);
		this.#currentLevel++;
		//console.log(level.matchings);
        //Object.values(this.currentLevel.matchings).forEach(
          //  (matching) => matching.resetCount());
    }

	#randomWastage(wastageType) {
		const selectedWastage = new Image();
		let random;
		
		switch(wastageType) {
			case 'rubbish':
				random = Math.floor(Math.random() * this.#wastageTypes.rubbish.length);
				selectedWastage.src = `./pairs-assets/${this.#wastageTypes.rubbish[random]}.png`;
				selectedWastage.alt = this.#wastageTypes.rubbish[random];
				selectedWastage.dataset.type = 'rubbish';
				this.#wastageTypes.rubbish.splice(random,1);
				break;
			case 'recycle':
				random = Math.floor(Math.random() * this.#wastageTypes.recycle.length);
				selectedWastage.src = `./pairs-assets/${this.#wastageTypes.recycle[random]}.png`;
				selectedWastage.alt = this.#wastageTypes.recycle[random];
				selectedWastage.dataset.type = 'recycle';
				this.#wastageTypes.recycle.splice(random,1);
				break;
			case 'food':
				random = Math.floor(Math.random() * this.#wastageTypes.food.length);
				selectedWastage.src = `./pairs-assets/${this.#wastageTypes.food[random]}.png`;
				selectedWastage.alt = this.#wastageTypes.food[random];
				selectedWastage.dataset.type = 'food';
				this.#wastageTypes.food.splice(random,1);
				break;
		}
		selectedWastage.hidden = false;
		return selectedWastage;
	}

    #randomEmoji(emojiSet) {
        var emojiIsValid;
        var generatedEmoji;
        do {
            emojiIsValid = true;
            generatedEmoji = Emoji.generateRandomEmoji(this.#hideEmojis);
            emojiSet.forEach((addedEmoji) => {
                if(addedEmoji.emojiID === generatedEmoji.emojiID)
                    emojiIsValid = false;
            });
        } while(!emojiIsValid);

        return generatedEmoji;
    }

    get #getLevelDetails() {
        const detailsMap = this.#levels.map((level) => level.details) 
        const details = {}
        detailsMap.forEach((level, index) => {
                details[`!${index + 1}`] = level;
        })
        //console.log(details);
        return details;
    }

    get #isGameComplete() {
        return this.#currentLevel === 3;
    }

    get #json() {
        return JSON.stringify({
            "difficulty": `_complex`,
            "_data": {
                "totalscore": this.totalScore,
                "totalmistakes": this.totalMistakes,
                "#@level" : this.#getLevelDetails
            }
        });
    }

    static {
        Game.#hide = false;
        Game.#hiddenEmoji = document.createElement("div");
        Game.#hiddenEmoji.className = "hidden";
        Game.#hiddenEmoji.hidden = true;
        Game.#hiddenEmoji.appendChild(document.createTextNode("?"));
    }
    #levels;
    #hideEmojis;
}

window.startGame = startGame;