# bizerror

Collections of common business errors.

## Install

    pip install bizerror

## Defined Errors

- BizError
- OK
- SysError
    - UndefinedError

- HttpError
    - RequestExpired
    - NotSupportedHttpMethod

- ConfigError
    - MissingConfigItem

- DataError
    - TargetNotFound

- AuthError
    - AccountLockedError
    - AccountTemporaryLockedError
    - UserPasswordError
    - AppAuthFailed
    - TsExpiredError
    - AccountDisabledError
    - AccountStatusError
    - AccountRemovedError

- TypeError
    - CastToIntegerFailed
    - CastToFloatFailed
    - CastToNumbericFailed
    - CastToBooleanFailed
    - CastToStringFailed
    - ParseJsonError

- ParamError
    - MissingParameter
    - BadParameter
    - BadParameterType

- FormError
    - CaptchaOnlyAllowedOnce
    - CaptchaValidateFailed

- LogicError


## Release Notes


### v0.1.0

- Add BizError base class.
- Add some common errors.
