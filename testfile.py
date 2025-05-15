from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import random
import pyaudio
import numpy as np
import requests

class MarioKartDSGame(Ursina):
    def __init__(self):
        super().__init__()

        try:
            import pyaudio
        except ImportError:
            print("MARIO SAYS: PYAUDIO NOT INSTALLED QUITTING TECH DEMO")
            return

        window.fps_counter.enabled = True
        window.exit_button.visible = False

        self.create_random_track()
        self.player = FirstPersonController(collider='box')
        camera.fov = 60  # Lower FOV to emulate a more "zoomed in" feel
        camera.clip_plane_near = 0.1  # Adjust near clipping plane
        self.generate_sound()
        self.karts = self.create_karts()

    def create_random_track(self):
        response = requests.get('https://randomuser.me/api/?results=10')
        data = response.json()

        Entity(model='plane', scale=(100, 1, 100), color=color.rgb(0, 255, 0), position=(0, -1, 0), collider='box')

        for i, result in enumerate(data['results']):
            x = hash(result['location']['street']['name']) % 20 - 10
            z = hash(result['location']['street']['number']) % 40 - 20
            Entity(model='cube', color=color.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), position=(x, 0, z), scale=(1, 2, 1), collider='box')

        for _ in range(10):
            x = random.randint(-15, 15)
            z = random.randint(-30, 30)
            Entity(model='sphere', color=color.rgb(255, 0, 0), position=(x, 1, z), scale=(1, 1, 1))

    def create_karts(self):
        karts = []
        for i in range(5):
            kart = Entity(model='cube', color=color.rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)), position=(random.randint(-10, 10), 1, random.randint(-30, 30)), scale=(1, 1, 1))
            karts.append(kart)
        return karts

    def generate_sound(self):
        import threading
        threading.Thread(target=self.play_sound).start()

    def play_sound(self):
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

    def update(self):
        for kart in self.karts:
            kart.x += random.uniform(-0.1, 0.1)
            kart.z += random.uniform(-0.1, 0.1)

if __name__ == "__main__":
    game = MarioKartDSGame()
    game.run()
