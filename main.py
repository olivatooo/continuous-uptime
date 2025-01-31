import imgui
import sdl2
import sdl2.ext
from imgui.integrations.sdl2 import SDL2Renderer


def main():
    imgui.create_context()
    window, renderer = impl_sdl2_init()
    impl = SDL2Renderer(window, renderer)

    gamemode = "Default"
    auto_update = False

    running = True
    while running:
        for event in sdl2.ext.get_events():
            if event.type == sdl2.SDL_QUIT:
                running = False
            impl.process_event(event)

        impl.process_inputs()

        imgui.new_frame()

        imgui.begin("Game Menu")

        if imgui.button("Start"):
            print("Game Started")

        imgui.text("Select Gamemode:")
        clicked, gamemode = imgui.combo(
            "##gamemode", gamemode, ["Default", "Easy", "Hard"]
        )

        _, auto_update = imgui.checkbox("Auto Update", auto_update)

        imgui.end()

        imgui.render()
        impl.render(imgui.get_draw_data())
        sdl2.SDL_RenderPresent(renderer)

    impl.shutdown()
    sdl2.SDL_DestroyRenderer(renderer)
    sdl2.SDL_DestroyWindow(window)
    sdl2.SDL_Quit()


def impl_sdl2_init():
    if sdl2.SDL_Init(sdl2.SDL_INIT_EVERYTHING) < 0:
        print(f"Error: SDL could not initialize! SDL Error: {sdl2.SDL_GetError()}")
        exit(1)

    window = sdl2.SDL_CreateWindow(
        b"ImGui Game Menu",
        sdl2.SDL_WINDOWPOS_CENTERED,
        sdl2.SDL_WINDOWPOS_CENTERED,
        800,
        600,
        sdl2.SDL_WINDOW_SHOWN,
    )

    if not window:
        print(f"Error: Window could not be created! SDL Error: {sdl2.SDL_GetError()}")
        exit(1)

    renderer = sdl2.SDL_CreateRenderer(window, -1, sdl2.SDL_RENDERER_ACCELERATED)
    if not renderer:
        print(f"Error: Renderer could not be created! SDL Error: {sdl2.SDL_GetError()}")
        exit(1)

    return window, renderer


if __name__ == "__main__":
    main()
