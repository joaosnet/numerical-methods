SECRET_KEY = "96ea35fc75f5213e3d33546f9e26af78baa9565e818b9285"

# gerador de chaves aleatórias
if __name__ == "__main__":
    import os
    print(os.urandom(24).hex())
