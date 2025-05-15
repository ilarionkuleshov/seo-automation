import streamlit as st


def example_image(text: str, image: str) -> None:
    """Displays an example image with provided text and image.

    Args:
        text (str): The text to display.
        image (str): The image to display.

    """

    @st.dialog("Example of result")
    def show_example() -> None:
        st.write(text)
        st.image(image)

    st.button("Example of result", icon="🖼", on_click=show_example, use_container_width=True)
