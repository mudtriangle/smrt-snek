class Board {
    constructor() {
        this.board = [];
        this.snek = [[0, 2], [0, 1], [0, 0]];
        this.food = [ceil(random(100)) - 1, ceil(random(100)) - 1];

        // 0: RIGHT, 1: LEFT, 2: DOWN, 3: UP.
        this.direction = 0;
        this.just_ate = false;
        this.score = 0;
        this.alive = true;
        this.populate_board();
    }

    draw(y_offset, x_offset, square_size) {
        stroke(0, 0, 0, 0);
        let vertical_location = y_offset;
        let horizontal_location;

        for (let y = 0; y < 100; y++) {
            horizontal_location = x_offset;
            for (let x = 0; x < 100; x++) {
                if (this.board[y][x] === 0) {
                    fill(240, 234, 214);

                } else if (this.board[y][x] === 1) {
                    fill(12, 10, 4);

                } else if (this.board[y][x] === 2) {
                    fill(255, 0, 0);
                }

                rect(vertical_location, horizontal_location, square_size, square_size);
                horizontal_location += ceil(square_size * 1.25);
            }
            vertical_location += ceil(square_size * 1.25);
        }
    }

    update() {
        if (!this.alive) {
            return;
        }

        let last_piece = this.snek.pop();

        if (this.direction === 0) {
            this.snek = [[this.snek[0][0], this.snek[0][1] + 1]].concat(this.snek);

            if (this.snek[0][1] > 99) {
                this.snek[0][1] = 99;
                this.alive = false;
            }

        } else if (this.direction === 1) {
            this.snek = [[this.snek[0][0], this.snek[0][1] - 1]].concat(this.snek);

            if (this.snek[0][1] < 0) {
                this.snek[0][1] = 0;
                this.alive = false;
            }

        } else if (this.direction === 2) {
            this.snek = [[this.snek[0][0] + 1, this.snek[0][1]]].concat(this.snek);

            if (this.snek[0][0] > 99) {
                this.snek[0][0] = 99;
                this.alive = false;
            }

        } else if (this.direction === 3) {
            this.snek = [[this.snek[0][0] - 1, this.snek[0][1]]].concat(this.snek);

            if (this.snek[0][0] < 0) {
                this.snek[0][0] = 0;
                this.alive = false;
            }
        }

        if (this.food[0] === this.snek[0][0] && this.food[1] === this.snek[0][1]) {
            this.just_ate = true;
        }

        if (this.just_ate) {
            this.just_ate = false;
            this.snek = this.snek.concat([last_piece]);
            this.food = [ceil(random(100)) - 1, ceil(random(100)) - 1];
            this.score++;
        }

        this.populate_board();
    }

    populate_board() {
        for (let y = 0; y < 100; y++) {
            this.board[y] = [];
            for (let x = 0; x < 100; x++) {
                this.board[y][x] = 0;
            }
        }

        this.board[this.food[1]][this.food[0]] = 2;

        for (let i = 0; i < this.snek.length; i++) {
            this.board[this.snek[i][1]][this.snek[i][0]] = 1;
        }
    }
}