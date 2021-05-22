const app = new PIXI.Application({
    width: 1024,
    height: 768,
    backgroundColor: 0xcccccc
});

document.body.appendChild(app.view);
const container = new PIXI.Container();


app.stage.addChild(container);

const bubble_texture = PIXI.Texture.from('static/images/bubble.png');

const bubble = new PIXI.Sprite(bubble_texture);
bubble.anchor.set(0.5);


container.addChild(bubble);


container.x = app.screen.width / 2;
container.y = app.screen.height / 2;
container.scale.set(0.1);

console.log(container);

// container.pivot.x = container.width / 2;
// container.pivot.y = container.height / 2;

app.ticker.add( (delta) => {
    container.x += 0.1 * delta
    container.rotation += 0.01 * delta
    // console.log(container.x)
})


