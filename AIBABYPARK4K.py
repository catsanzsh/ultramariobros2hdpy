from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import pyaudio
import numpy as np

def main():
    try:
        import pyaudio
    except ImportError:
        print("MARIO SAYS: PYAUDIO NOT INSTALLED QUITTING TECH DEMO")
        return

    app = Ursina()

    window.fps_counter.enabled = True
    window.exit_button.visible = False

    def create_baby_park_track():
        # Base of the track
        Entity(model='plane', scale=(100, 1, 100), color=color.rgb(0, 255, 0), position=(0, -1, 0), collider='box')

        # Track boundaries
        for z in range(-40, 41):
            Entity(model='cube', color=color.rgb(255, 255, 255), position=(-20, 0, z), scale=(1, 2, 1), collider='box')
            Entity(model='cube', color=color.rgb(255, 255, 255), position=(20, 0, z), scale=(1, 2, 1), collider='box')

        # Turns and straights
        for x in range(-15, 16):
            Entity(model='cube', color=color.rgb(255, 255, 255), position=(x, 0, -40), scale=(1, 2, 1), collider='box')
            Entity(model='cube', color=color.rgb(255, 255, 255), position=(x, 0, 40), scale=(1, 2, 1), collider='box')

        # Baby Park-like features
        for _ in range(10):
            x = random.randint(-15, 15)
            z = random.randint(-30, 30)
            Entity(model='sphere', color=color.rgb(255, 0, 0), position=(x, 1, z), scale=(1, 1, 1))

    create_baby_park_track()

    player = FirstPersonController(collider='box')

    # Attempt to emulate Mario Kart-like rendering
    from ursina import camera
    camera.fov = 60  # Lower FOV to emulate a more "zoomed in" feel
    camera.clip_plane_near = 0.1  # Adjust near clipping plane

    # Generate sound
    def generate_sound():
        p = pyaudio.PyAudio()
        stream = p.open(format=pyaudio.paFloat32,
                        channels=1,
                        rate=44100,
                        output=True)

        frequency = 440  # Hz, waves per second
        duration = 10  # second

        samples = (np.sin(2 * np.pi * np.arange(44100 * duration) * frequency / 44100)).astype(np.float32)

        stream.write(samples)

        stream.stop_stream()
        stream.close()
        p.terminate()

    import threading
    threading.Thread(target=generate_sound).start()

    app.run()

if __name__ == "__main__":
    main()
