// Authored by Dan & Jack

import Level from "./level.js";

"use strict";

// Get element IDs
var backgroundLoop = document.getElementById("background-loop");
var gameOver = document.getElementById("game-over");
var incorrectMatch = document.getElementById("incorrect-match");
var correctMatch = document.getElementById("correct-match");

// Function to start the pairs game
function startGame() {
    // Get element IDs
    const game = new Game(false);
    const divPairs = document.getElementById("divPairs");
    const tblPairs = document.createElement("table");
    tblPairs.id = "tblPairs";
    
    // Hide elements
    document.getElementById("btnStartGame").remove();
    document.getElementById("buttonDiv").hidden = true;
	document.getElementById("ftrSources").hidden = true;
	document.getElementById('btnSources').hidden = true;

    // Play music and load sfx audio
    backgroundLoop.play();
    gameOver.load();
    incorrectMatch.load();
    correctMatch.load();
    
    // Start game level
    divPairs.append(tblPairs);
    game.loadNextLevel();
}

// Function to flip a card
function flipCard(card, currentLevel) {
    if(Level.resetting || card.dataset.isFlipped === "true") return;

    currentLevel.flippedCards.push(card);
    // Check if card is the same type as those already in flipped cards
    if(card.dataset.type === currentLevel.flippedCards[0].dataset.type) {
        card.dataset.isFlipped = true;

        // All cards are matched
        if(currentLevel.flippedCards.length == currentLevel.matchings[card.dataset.type]) {
            for(let flippedCard of currentLevel.flippedCards)
                flippedCard.style.backgroundColor = 'gold';
            // Play sfx
            correctMatch.play();
            currentLevel.addScore();
            currentLevel.completeMatching(card.dataset.type);
            // Empty currentLevel.flippedCards
            currentLevel.resetFlipped(); 
        }
    } else {
        // Selected card does not follow current matching
        incorrectMatch.play();
        currentLevel.addMistake();
        for(let flippedCard of currentLevel.flippedCards)
            flippedCard.style.backgroundColor = "red";
        resetCards(currentLevel);
    }
}

// Function to choose which waste items to show
function chooseWastage(matches) {
	const keys = Object.keys(matches);
	
	var wastage;
    do {
        wastage = keys[Math.floor(Math.random() * keys.length)];
    } while(matches[wastage].length == 0);
	
	// Picks random image
	const random = Math.floor(Math.random() * matches[wastage].length);
	const chosenWastage = matches[wastage][random];
	matches[wastage].splice(random,1);
    
    return chosenWastage;
}

// Function to reset cards
async function resetCards(currentLevel) {
    Level.resetting = true;
    // Wait 3 seconds
    await new Promise(resolve => setTimeout(resolve, 3000));

    // Reset flipped cards
    for(let flippedCard of currentLevel.flippedCards) {
        flippedCard.style.backgroundColor = "white";
        flippedCard.dataset.isFlipped = false;
    }
    currentLevel.resetFlipped();
    Level.resetting = false;
}

// Function to get card shape
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

// Game class
class Game {
    // Get image urls from static
    // Urls defined in the html script section to access static files
    #wastageTypes = {
		rubbish: ['toiletRollImageURL','plasticBagImageURL','blueRollImageURL'],
		recycle: ['cardboardImageURL','plasticBottleImageURL','paperImageURL'],
		food: ['bananaImageURL','meatImageURL','eggplantImageURL']
	};
	#completedMatchings;
	#currentLevel;

    // Constuctor to make board
    constructor() {
		let level1, level2, level3;
		let matchings1,matchings2,matchings3;
		let rubbishImage, recycleImage, foodImage;
		
		this.#currentLevel = 0;
		this.#completedMatchings = new Array();
		
		rubbishImage = new Image();
		rubbishImage.src = rubbishImageURL;
		rubbishImage.alt = 'rubbish';
		rubbishImage.dataset.type = 'rubbish';
		rubbishImage.hidden = false;
		
		recycleImage = new Image();
		recycleImage.src = recycleImageURL;
		recycleImage.alt = 'recycle';
		recycleImage.dataset.type = 'recycle';
		recycleImage.hidden = false;
		
		foodImage = new Image();
		foodImage.src = foodImageURL;
		foodImage.alt = 'food';
		foodImage.dataset.type = 'food';
		foodImage.hidden = false;
		
		// Select 2 random from rubbish and recycle here
		
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
		
		// Add food selection here
		let foodSelection = [foodImage, this.#randomWastage('food'),this.#randomWastage('food')];
		matchings2.food = foodSelection;
		
		matchings3 = {
			'rubbish': [...rubbishSelection],
			'recycle': [...recycleSelection],
			'food': [...foodSelection]
		};
		
		// Appends last item in arrays
		matchings3['rubbish'].push(this.#randomWastage('rubbish'));
		matchings3['recycle'].push(this.#randomWastage('recycle'));
		matchings3['food'].push(this.#randomWastage('food'));
	
		level1 = new Level(matchings1);
		level2 = new Level(matchings2);
		level3 = new Level(matchings3);
        this.#levels = [level1, level2, level3];
    }

    // Function to get the total level score
    get totalScore() {
        return this.#levels.map(
            (level) => level.score).reduce(
                (accScore, currentScore) => accScore + currentScore
            );
    }

    // Function to get the number of mistakes made
    get totalMistakes() {
        return this.#levels.map(
            (level) => level.mistakes).reduce(
                (accMistakes, currentMistakeCount) => accMistakes + currentMistakeCount  
            );
    }

    // Function to get the game levels
    get levels() {
        return this.#levels;
    }

    // Load the next level
    loadNextLevel() {
		let level = this.#levels[this.#currentLevel];
        let tblPairs = document.getElementById("tblPairs");
        let shape = getShape(level.matchings);
        let typeCount = level.matchings['rubbish'].length;
		
        // Clear table for upcoming level
        Object.values(tblPairs.getElementsByTagName("tr")).forEach(
            (child) => child.remove());
		
		
        // Generate table
        for(let i = 0; i < shape[0]; i++) {
            const row = tblPairs.insertRow();
            for(let j = 0; j < shape[1]; j++) {
                const cell = row.insertCell();
                const card = document.createElement("div");
                const wastage = chooseWastage(level.matchings);
                card.className = 'card';
                card.dataset.isFlipped = false;
				card.dataset.type = wastage.dataset.type;
				
                // Card click listener
                card.onclick = () => {
                    flipCard(card, level);
                    if(level.isLevelComplete()) {
                        // Check if game is complete
                        if(this.#isGameComplete) {
                            // Hide game table
                            tblPairs.hidden = true;

                            // Get elements and show/hide as necessary
                            var finalScoreDiv = document.getElementById("finalScoreDiv");
                            var finalScore = document.getElementById("finalScore");
                            var btnEndGame = document.getElementById("btnEndGame");
                            document.getElementById("buttonDiv").hidden = false;
                            document.getElementById("divTitle").hidden = true;
                            finalScoreDiv.hidden = false;
                            finalScore.hidden = false;
                            btnEndGame.hidden = false;

                            // Get and display score
                            var data = JSON.parse(this.#json);
                            finalScore.innerHTML = "Score: " + data.totalscore;
                            document.getElementById("score").value = data.totalscore;

                            // Stop background music and play game complete sfx
                            backgroundLoop.pause();
                            gameOver.play();
                        } else {
                            this.loadNextLevel();
                        }
                    }
                }
				if(card !== "undefined" && wastage !== 'undefined')
					card.append(wastage.cloneNode(true));
                cell.appendChild(card);
            }
        }

		for(let type of Object.keys(level.matchings))
			level.matchings[type] = typeCount;
		this.#currentLevel++;
    }

    // Used to switch type of waste
	#randomWastage(wastageType) {
		const selectedWastage = new Image();
		let random;
		
		switch(wastageType) {
			case 'rubbish':
				random = Math.floor(Math.random() * this.#wastageTypes.rubbish.length);
                selectedWastage.src = eval(`${this.#wastageTypes.rubbish[random]}`);
				selectedWastage.alt = this.#wastageTypes.rubbish[random];
				selectedWastage.dataset.type = 'rubbish';
				this.#wastageTypes.rubbish.splice(random,1);
				break;
			case 'recycle':
				random = Math.floor(Math.random() * this.#wastageTypes.recycle.length);
                selectedWastage.src = eval(`${this.#wastageTypes.recycle[random]}`);
				selectedWastage.alt = this.#wastageTypes.recycle[random];
				selectedWastage.dataset.type = 'recycle';
				this.#wastageTypes.recycle.splice(random,1);
				break;
			case 'food':
				random = Math.floor(Math.random() * this.#wastageTypes.food.length);
                selectedWastage.src = eval(`${this.#wastageTypes.food[random]}`);
				selectedWastage.alt = this.#wastageTypes.food[random];
				selectedWastage.dataset.type = 'food';
				this.#wastageTypes.food.splice(random,1);
				break;
		}
		selectedWastage.hidden = false;
		return selectedWastage;
	}

	// Provides level individual details like score for level and number of mistakes made
    get #getLevelDetails() {
        const detailsMap = this.#levels.map((level) => level.details) 
        const details = {}
        detailsMap.forEach((level, index) => {
                details[`!${index + 1}`] = level;
        })
        return details;
    }

	// If the three levels have been completed, end the game
    get #isGameComplete() {
        return this.#currentLevel === 3;
    }

    get #json() {
        return JSON.stringify({
			"totalscore": this.totalScore,
			"totalmistakes": this.totalMistakes,
			"level" : this.#getLevelDetails
        });
    }

    #levels;
}

// Start the game
window.startGame = startGame;