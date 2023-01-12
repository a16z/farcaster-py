import os

from dotenv import load_dotenv

from farcaster.client import MerkleApiClient

load_dotenv()

fcc = MerkleApiClient(access_token=os.getenv("AUTH"))


def test_get_cast():
    # get cast
    response = fcc.get_cast("0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f")
    print(response)
    assert (
        response.result.cast.author.fid
        == 3
    )

def test_get_all_casts_in_thread():
    # get cast
    response = fcc.get_all_casts_in_thread("0x321712dc8eccc5d2be38e38c1ef0c8916c49949a80ffe20ec5752bb23ea4d86f")
    print(response)
    assert (
        response.result.casts[0].author.fid
        == 3
    )

# def test_get_host_addr():
#     # get user's host address
#     assert (
#         fcc.get_host_addr("v")
#         == "https://guardian.farcaster.xyz/origin/directory/0x012D3606bAe7aebF03a04F8802c561330eAce70A"
#     )


# def test_get_profile():
#     # get user's profile
#     profile = fcc.get_profile("v")
#     assert (
#         profile.merkle_root
#         == "0xe766d07229f933a12ec12e91e7effb6e06cea69d79666c5e95cc2ccdb94960f3"
#     )


# def test_get_casts():
#     # get user's casts
#     casts = fcc.get_casts("v")
#     assert (
#         casts[-1].merkle_root
#         == "0x1da27f3cdae7a3d439a4487cb53b5d61d47c1007f6c85d4e26e741acefd7a605"
#     )


# def test_get_username():
#     username = fcc.get_username("0x012D3606bAe7aebF03a04F8802c561330eAce70A")
#     assert username == "v"


# def test_verify_casts():
#     casts = fcc.get_casts("v")
#     # verify cast
#     assert fcc.verify_cast(casts[-1])
