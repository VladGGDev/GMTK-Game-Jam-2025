import engine
import game.scenes.carscene, tests.uitestscene


# Setup
engine.unscaled_fixed_delta_time = 1 / 144
engine.run(
    engine.SceneManager(
        {
            "UI" : tests.uitestscene.UiTestScene(),
            "Car" : game.scenes.carscene.CarScene(),
        },
        "Car"
    ),
    {
        # "Main" : engine.DrawPass((320, 180), 0, None, (254, 231, 97, 255)),
        "Main" : engine.DrawPass((640, 360), 0, None, (254, 231, 97, 255)),
        "UI" : engine.DrawPass.create_ui((640, 360), 99)
    },
    True)
