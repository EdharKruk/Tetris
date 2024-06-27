const canvas = document.getElementById('gameCanvas');
const ctx = canvas.getContext('2d');
const nextPieceCanvas = document.getElementById('nextPieceCanvas');
const nextCtx = nextPieceCanvas.getContext('2d');
let playerName = '';

document.addEventListener('DOMContentLoaded', () => {
    document.getElementById('nameInput').style.display = 'block';
    document.getElementById('gameContainer').style.display = 'none';
});

function startGame() {
    playerName = document.getElementById('playerName').value;
    document.getElementById('nameInput').style.display = 'none';
    document.getElementById('gameContainer').style.display = 'flex';
    initGame();
}

const ROWS = 20;
const COLS = 10;
const BLOCK_SIZE = 30;
const SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[1, 1, 1], [0, 1, 0]],
    [[1, 1, 1], [1, 0, 0]],
];

const COLORS = ['cyan', 'yellow', 'purple', 'green', 'red', 'blue', 'orange'];

let grid = createGrid();
let currentPiece = getRandomPiece();
let nextPiece = getRandomPiece();
let score = 0;
let gameOver = false;
let dropStart = Date.now();
const dropInterval = 1000; 

function createGrid() {
    return Array.from({ length: ROWS }, () => Array(COLS).fill(0));
}

function drawGrid() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    for (let r = 0; r < ROWS; r++) {
        for (let c = 0; c < COLS; c++) {
            if (grid[r][c]) {
                ctx.fillStyle = COLORS[grid[r][c] - 1];
                ctx.fillRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                ctx.strokeRect(c * BLOCK_SIZE, r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function getRandomPiece() {
    const shapeIndex = Math.floor(Math.random() * SHAPES.length);
    return {
        shape: SHAPES[shapeIndex],
        color: COLORS[shapeIndex],
        x: Math.floor(COLS / 2) - 1,
        y: 0,
    };
}

function drawPiece(piece) {
    ctx.fillStyle = piece.color;
    for (let r = 0; r < piece.shape.length; r++) {
        for (let c = 0; c < piece.shape[r].length; c++) {
            if (piece.shape[r][c]) {
                ctx.fillRect((piece.x + c) * BLOCK_SIZE, (piece.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                ctx.strokeRect((piece.x + c) * BLOCK_SIZE, (piece.y + r) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function movePiece(dx, dy) {
    currentPiece.x += dx;
    currentPiece.y += dy;
    if (!isValidMove(currentPiece)) {
        currentPiece.x -= dx;
        currentPiece.y -= dy;
        return false;
    }
    return true;
}

function isValidMove(piece) {
    for (let r = 0; r < piece.shape.length; r++) {
        for (let c = 0; c < piece.shape[r].length; c++) {
            if (piece.shape[r][c]) {
                const newX = piece.x + c;
                const newY = piece.y + r;
                if (newX < 0 || newX >= COLS || newY >= ROWS || (newY >= 0 && grid[newY][newX])) {
                    return false;
                }
            }
        }
    }
    return true;
}

function placePiece() {
    for (let r = 0; r < currentPiece.shape.length; r++) {
        for (let c = 0; c < currentPiece.shape[r].length; c++) {
            if (currentPiece.shape[r][c]) {
                if (currentPiece.y + r < 0) {
                    console.log("Game Over condition met in placePiece function.");
                    gameOver = true;
                    drawGameOver();
                    return;
                }
                grid[currentPiece.y + r][currentPiece.x + c] = COLORS.indexOf(currentPiece.color) + 1;
            }
        }
    }
    currentPiece = nextPiece;
    nextPiece = getRandomPiece();
}

function clearLines() {
    outer: for (let r = ROWS - 1; r >= 0; r--) {
        for (let c = 0; c < COLS; c++) {
            if (!grid[r][c]) {
                continue outer;
            }
        }
        grid.splice(r, 1);
        grid.unshift(Array(COLS).fill(0));
        score += 10;
    }
}

function update() {
    if (gameOver) {
        console.log("Game over state detected in update function.");
        return;
    }
    const now = Date.now();
    if (now - dropStart >= dropInterval) {
        dropStart = now;
        if (!movePiece(0, 1)) {
            placePiece();
            clearLines();
            if (!isValidMove(currentPiece)) {
                console.log("Game Over condition met in update function.");
                gameOver = true;
                drawGameOver();
            }
        }
    }
}

function drawGameOver() {
    console.log("Drawing Game Over message.");
    ctx.clearRect(0, 0, canvas.width, canvas.height); 
    ctx.fillStyle = 'black'; 
    ctx.fillRect(0, 0, canvas.width, canvas.height); 
    ctx.fillStyle = 'red';  
    ctx.font = '50px Arial';  
    ctx.fillText('Game Over', canvas.width / 2 - 150, canvas.height / 2);
    saveScore();
    setTimeout(() => {
        document.addEventListener('keydown', handleRestart);
    }, 3000);  
}

function handleRestart(event) {
    if (event.key === 'Enter') {
        restartGame();
    }
}

function saveScore() {
    fetch('/save_score', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: playerName, score: score }),
    }).then((response) => response.json())
      .then((data) => {
          if (data.status === 'success') {
              console.log('Score saved successfully');
          } else {
              console.error('Error saving score');
          }
      }).catch((error) => {
          console.error('Error:', error);
      });
}

function gameLoop() {
    update();
    drawGrid();
    drawPiece(currentPiece);
    drawNextPiece(nextPiece); 
    drawUI();
    if (!gameOver) {
        requestAnimationFrame(gameLoop);
    }
}

function initGame() {
    grid = createGrid();
    currentPiece = getRandomPiece();
    nextPiece = getRandomPiece();
    score = 0;
    dropStart = Date.now();
    gameOver = false;
    gameLoop();
    document.addEventListener('keydown', handleKeydown);
}

function handleKeydown(event) {
    if (!gameOver) {
        if (event.key === 'ArrowLeft') {
            movePiece(-1, 0);
        } else if (event.key === 'ArrowRight') {
            movePiece(1, 0);
        } else if (event.key === 'ArrowDown') {
            movePiece(0, 1);
        } else if (event.key === 'ArrowUp') {
            rotatePiece();
        }
    }
}

function rotatePiece() {
    const shape = currentPiece.shape;
    const newShape = shape[0].map((_, index) => shape.map(row => row[index]).reverse());
    const backup = currentPiece.shape;
    currentPiece.shape = newShape;
    if (!isValidMove(currentPiece)) {
        currentPiece.shape = backup;
    }
}

function drawNextPiece(piece) {
    nextCtx.clearRect(0, 0, nextPieceCanvas.width, nextPieceCanvas.height); 
    nextCtx.fillStyle = piece.color;
    const offsetX = (nextPieceCanvas.width - piece.shape[0].length * BLOCK_SIZE) / 2;
    const offsetY = (nextPieceCanvas.height - piece.shape.length * BLOCK_SIZE) / 2;
    for (let r = 0; r < piece.shape.length; r++) {
        for (let c = 0; c < piece.shape[r].length; c++) {
            if (piece.shape[r][c]) {
                nextCtx.fillRect(offsetX + c * BLOCK_SIZE, offsetY + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
                nextCtx.strokeRect(offsetX + c * BLOCK_SIZE, offsetY + r * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE);
            }
        }
    }
}

function drawUI() {
    ctx.font = '20px Arial';
    ctx.fillStyle = 'black';
    ctx.fillText(`Player: ${playerName}`, 10, 20);
    ctx.fillText(`Score: ${score}`, 10, 50);
}

function restartGame() {
    console.log("Restarting game.");
    document.removeEventListener('keydown', handleRestart);
    document.getElementById('nameInput').style.display = 'block';
    document.getElementById('gameContainer').style.display = 'none';
}
