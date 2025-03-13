from cx_Freeze import setup, Executable

# Thay đổi tên và mô tả cho ứng dụng của bạn
setup(
    name="checkUseAI",
    version="0.1",
    description="Mô tả ứng dụng của bạn",
    executables=[Executable("demo.py")],  # Thay 'your_program.py' bằng tên tệp của bạn
)