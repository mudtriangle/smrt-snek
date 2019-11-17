let ai_board;
let user_board;
let game_started;

function setup() {
    createCanvas(1430, 700);

    ai_board = new Board('../src_model/play.py');
    user_board = new Board('human');

    game_started = false;
}

function draw() {
    background(255, 255, 255);
    if (!game_started) {
        fill(0, 0, 0);
        textStyle(NORMAL);
        textSize(32);
        textAlign(CENTER, TOP);
        text('Press space bar to start.', 0, 12, width);

    } else {
        ai_board.draw(0, 0, 5);
        user_board.draw(720, 0, 5);
        // ai_board.update();
        // user_board.update();
    }
}

function keyPressed() {
    if (!game_started) {
        if (key === ' ') {
            game_started = true;
        }

    } else {
        if (key === 'r') {
            game_started = false;
            // ai_board = new Board('../src_model/play.py');
            // user_board = new Board('human');
        }
    }
}
