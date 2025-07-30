import engine
import tests.camtestscene, tests.tweentestscene, tests.turntest, tests.uitestscene


# Setup
engine.run(
    engine.SceneManager(
        {
            "Tweening" : tests.tweentestscene.TweenTestScene(),
            "Camera" : tests.camtestscene.CameraTestScene(),
            "Turn" : tests.turntest.TurnTestScene(),
            "UI" : tests.uitestscene.UiTestScene()
        },
        "UI"
    ),
    {
        "Main" : engine.DrawPass((256, 256), 0, None, (128, 128, 128, 255)),
        "UI" : engine.DrawPass.create_ui((256, 256), 0)
    })
