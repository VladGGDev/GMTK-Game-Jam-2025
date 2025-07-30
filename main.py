import engine
import tests.cartestscene, tests.uitestscene


# Setup
engine.run(
    engine.SceneManager(
        {
            "Car" : tests.cartestscene.CarTestScene(),
            "UI" : tests.uitestscene.UiTestScene()
        },
        "Car"
    ),
    {
        "Main" : engine.DrawPass((320, 180), 0, None, (254, 231, 97, 255)),
        "UI" : engine.DrawPass.create_ui((320, 180), 99)
    },
    True)
