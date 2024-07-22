const canvas = document.querySelector('canvas');
const c = canvas.getContext('2d');
const scoreEl = document.querySelector('#scoreEl');
const gameContainer = document.querySelector('.game-container');

function resizeCanvas() {
    canvas.width = window.innerWidth * 0.8;
    canvas.height = window.innerHeight * 0.8;
}

window.addEventListener('resize', resizeCanvas);
resizeCanvas();

const pellets = [];
const powerUps = [];
const ghosts = [
    new Ghost({
        position: {
            x: Boundary.width * 6 + Boundary.width / 2,
            y: Boundary.height + Boundary.height / 2,
        },
        velocity: {
            x: Ghost.speed,
            y: 0,
        },
    }),
    new Ghost({
        position: {
            x: Boundary.width * 6 + Boundary.width / 2,
            y: Boundary.height * 3 + Boundary.height / 2,
        },
        velocity: {
            x: Ghost.speed,
            y: 0,
        },
        color: 'pink',
    }),
];

const player = new Player({
    position: {
        x: Boundary.width + Boundary.width / 2,
        y: Boundary.height + Boundary.height / 2,
    },
    velocity: {
        x: 0,
        y: 0,
    },
});

const keys = {
    w: {
        pressed: false,
    },
    a: {
        pressed: false,
    },
    s: {
        pressed: false,
    },
    d: {
        pressed: false,
    },
};

let lastKey = '';
let score = 0;
let animationId;

const boundaries = generateBoundaries();

function animate() {
    animationId = requestAnimationFrame(animate);
    c.clearRect(0, 0, canvas.width, canvas.height);

    if (keys.w.pressed && lastKey === 'w') player.moveUp(boundaries);
    else if (keys.a.pressed && lastKey === 'a') player.moveLeft(boundaries);
    else if (keys.s.pressed && lastKey === 's') player.moveDown(boundaries);
    else if (keys.d.pressed && lastKey === 'd') player.moveRight(boundaries);

    for (let i = ghosts.length - 1; i >= 0; i--) {
        const ghost = ghosts[i];
        if (Math.hypot(ghost.position.x - player.position.x, ghost.position.y - player.position.y) <
            ghost.radius + player.radius) {
            if (ghost.scared) {
                ghosts.splice(i, 1);
            } else {
                cancelAnimationFrame(animationId);
                console.log('you lose');
            }
        }
    }

    if (pellets.length === 0) {
        console.log('you win');
        cancelAnimationFrame(animationId);
    }

    for (let i = powerUps.length - 1; i >= 0; i--) {
        const powerUp = powerUps[i];
        powerUp.draw();

        if (Math.hypot(powerUp.position.x - player.position.x, powerUp.position.y - player.position.y) <
            powerUp.radius + player.radius) {
            powerUps.splice(i, 1);
            ghosts.forEach((ghost) => {
                ghost.scared = true;
                setTimeout(() => {
                    ghost.scared = false;
                }, 5000);
            });
        }
    }

    for (let i = pellets.length - 1; i >= 0; i--) {
        const pellet = pellets[i];
        pellet.draw();

        if (Math.hypot(pellet.position.x - player.position.x, pellet.position.y - player.position.y) <
            pellet.radius + player.radius) {
            pellets.splice(i, 1);
            score += 10;
            scoreEl.innerHTML = score;
        }
    }

    boundaries.forEach((boundary) => {
        boundary.draw();
        if (circleCollidesWithRectangle({
            circle: player,
            rectangle: boundary,
        })) {
            player.velocity.x = 0;
            player.velocity.y = 0;
        }
    });
    player.update();

    ghosts.forEach((ghost) => {
        ghost.update();
        const collisions = [];
        boundaries.forEach((boundary) => {
            if (!collisions.includes('right') && circleCollidesWithRectangle({
                circle: {
                    ...ghost,
                    velocity: {
                        x: ghost.speed,
                        y: 0,
                    },
                },
                rectangle: boundary,
            })) {
                collisions.push('right');
            }

            if (!collisions.includes('left') && circleCollidesWithRectangle({
                circle: {
                    ...ghost,
                    velocity: {
                        x: -ghost.speed,
                        y: 0,
                    },
                },
                rectangle: boundary,
            })) {
                collisions.push('left');
            }

            if (!collisions.includes('up') && circleCollidesWithRectangle({
                circle: {
                    ...ghost,
                    velocity: {
                        x: 0,
                        y: -ghost.speed,
                    },
                },
                rectangle: boundary,
            })) {
                collisions.push('up');
            }

            if (!collisions.includes('down') && circleCollidesWithRectangle({
                circle: {
                    ...ghost,
                    velocity: {
                        x: 0,
                        y: ghost.speed,
                    },
                },
                rectangle: boundary,
            })) {
                collisions.push('down');
            }
        });

        if (collisions.length > ghost.prevCollisions.length)
            ghost.prevCollisions = collisions;

        if (JSON.stringify(collisions) !== JSON.stringify(ghost.prevCollisions)) {
            if (ghost.velocity.x > 0) ghost.prevCollisions.push('right');
            else if (ghost.velocity.x < 0) ghost.prevCollisions.push('left');
            else if (ghost.velocity.y < 0) ghost.prevCollisions.push('up');
            else if (ghost.velocity.y > 0) ghost.prevCollisions.push('down');

            const pathways = ghost.prevCollisions.filter((collision) => !collisions.includes(collision));
            const direction = pathways[Math.floor(Math.random() * pathways.length)];

            switch (direction) {
                case 'down':
                    ghost.velocity.y = ghost.speed;
                    ghost.velocity.x = 0;
                    break;
                case 'up':
                    ghost.velocity.y = -ghost.speed;
                    ghost.velocity.x = 0;
                    break;
                case 'right':
                    ghost.velocity.y = 0;
                    ghost.velocity.x = ghost.speed;
                    break;
                case 'left':
                    ghost.velocity.y = 0;
                    ghost.velocity.x = -ghost.speed;
                    break;
            }

            ghost.prevCollisions = [];
        }
    });

    if (player.velocity.x > 0) player.rotation = 0;
    else if (player.velocity.x < 0) player.rotation = Math.PI;
    else if (player.velocity.y > 0) player.rotation = Math.PI / 2;
    else if (player.velocity.y < 0) player.rotation = Math.PI * 1.5;
}

animate();
