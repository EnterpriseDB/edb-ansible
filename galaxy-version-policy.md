
- version structure

            □   .   ■   .   ◆   -   △
          Major   Minor   Patch    pre
                                -release

1. Major version Rule

    - Major version zero (0.y.z) is for initial development.
    - After version 1.0.0, It can be production.
    - Same major version(Xyz | x=x') must be compatible.
    - When a version of a product must be released, it upgrades the major version.
    - Version upgrade if a fuction that is not compatible with the lower version (Xyz | X>0) is added.


2. Minor version Rule

    - There should be no crashes when running the same minor version(xYz | y=y').
    - Version upgrade when critical errors are corrected.
      - e.g. Unexpected behavior, abnormal termination, etc.
    - Version upgrade if a fuction that is compatible with the lower version (xYz | x>0) is added.


3. Patch version Rule

    - Version upgrade when bug fixed.
    - Version upgrade when modified uncritical error on IMS issue.
    - Version upgrade when README.md is modified
    - Version upgarde when internal behavior is modified. It is not change user action in same minor version.
    - Version upgrade when code prettifier.
    - Version upgrade when test framework is modified.


4. pre-release version Rule

    - It is not necessary to specify the pre-release version.
    - Can be marked with [0-9A-Za-z-] combination after additional "-" (hypen) after Patch version(xyz-p).
    - Separate each pre-release letter with a "." (dot).
    - The pre-release version cannot be expressed as an empty string when specified.
    - In the case of pre-release, the version is lower than the general version unconditionally(2.0.0-a < 2.0.0).
    - e.g. 2.0.0-a, 2.0.0-1.alpha

When the major version is changed, the minor version becomes 0. And when the minor version is changed, the patch version becomes 0. 
The version number increases sequentially.