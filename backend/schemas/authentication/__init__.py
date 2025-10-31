from pydantic import BaseModel, Field, field_validator


class LoginRequest(BaseModel):
    username: str
    password: str = Field(min_length=5)


class ForgetPasswordRequest(BaseModel):
    username: str
    new_user: bool
    new_password: str = Field(min_length=5)

    @field_validator("new_user")
    def assert_new_user_is_true(cls, value: bool):
        if value is not True:
            raise ValueError("`new_user` must be true!")
        return value
