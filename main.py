import engine
import game.scenes.carscene, tests.uitestscene, tests.circlecollisionsolvertestscene,tests.shaketest


# Setup
engine.unscaled_fixed_delta_time = 1 / 144
engine.set_window_title("GMTK Loop")
engine.run(
    engine.SceneManager(
        {
            # Tests
            "Coll solver": tests.circlecollisionsolvertestscene.CircleCollisionSolverTestScene(),
            "UI" : tests.uitestscene.UiTestScene(),
            
            "Car" : game.scenes.carscene.CarScene(),
            "Camera Shake" : tests.shaketest.ShakeTest(),
        },
        "Car"
    ),
    {
        # "Main" : engine.DrawPass((320, 180), 0, None, (254, 231, 97, 255)),
        "Main" : engine.DrawPass((480, 270), 0, None, (254, 231, 97, 255)),
        "UI" : engine.DrawPass.create_ui((480, 270), 99)
        
    },
    # True)
    False, default_window_size=(800, 500))
