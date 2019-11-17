class Walker {
    /*
    Random walker.
     */
    constructor(red, green, blue, stroke_weight, init_x, init_y) {
        /*
        Take RGB values, stroke weight (or thickness), and initial position.
         */
        this.x = init_x;
        this.y = init_y;
        this.r = red;
        this.g = green;
        this.b = blue;
        this.stroke_weight = stroke_weight;
    }

    display() {
        /*
        Show walker on screen as a point.
         */
        stroke(this.r, this.g, this.b, 10);
        strokeWeight(this.stroke_weight);
        point(this.x, this.y);
    }

    step() {
        /*
        Update the position of the walker randomly.
         */
        let choice = floor(random(4));

        // Choose a direction randomly (up, down, left, or right).
        if (choice == 0) {
            this.x += this.stroke_weight;
        } else if (choice == 1) {
            this.x -= this.stroke_weight;
        } else if (choice == 2) {
            this.y += this.stroke_weight;
        } else {
            this.y -= this.stroke_weight;
        }

        // If the walker would get out of the screen, force it back in.
        if (this.x < 0) {
            this.x = 0;
        } else if (this.x > 800) {
            this.x = 800;
        } else if (this.y < 0) {
            this.y = 0;
        } else if (this.y > 800) {
            this.y = 800;
        }
    }
}

let walkers;
let weight;

function setup() {
    createCanvas(800, 800);

    weight = 25;

    // Initialize walkers of colours red, green, blue, and white.
    walkers = [new Walker(255, 0, 0, weight, 300, 300),
               new Walker(0, 255, 0, weight, 500, 300),
               new Walker(0, 0, 255, weight, 300, 500),
               new Walker(255, 255, 255, weight, 500, 500)];

    background(253, 247, 194);
}

function draw() {
    // At each step, update each walker and also draw it on screen.
    for (let i = 0; i < walkers.length; i++) {
        walkers[i].step();
        walkers[i].display();
    }
}
