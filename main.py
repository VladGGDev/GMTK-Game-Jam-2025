import engine
import tests.uitestscene, tests.circlecollisionsolvertestscene,tests.shaketest
import game.scenes.carscene, game.scenes.mainmenuscene
    


# Setup
engine.unscaled_fixed_delta_time = 1 / 144
engine.set_window_title("GMTK Loop")
engine.run(
    engine.SceneManager(
        {
            # Tests
            "Coll solver": (tests.circlecollisionsolvertestscene.CircleCollisionSolverTestScene, ()),
            "UI" : (tests.uitestscene.UiTestScene, ()),
            "Camera Shake" : (tests.shaketest.ShakeTest, ()),
            
            # Game
            "Car" : (game.scenes.carscene.CarScene, ()),
            "Main Menu" : (game.scenes.mainmenuscene.MainMenuScene, ()),
        },
        "Main Menu"
    ),
    {
        "Main" : engine.DrawPass((480, 270), 0, None, (252, 221, 102, 255)),
        "UI" : engine.DrawPass.create_ui((480, 270), 0, (0, 0, 0, 0))
    },
    True)
    # False, default_window_size=(1000, 700))
    # False)
