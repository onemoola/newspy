## [2.2.16](https://github.com/onemoola/newspy/compare/v2.2.15...v2.2.16) (2025-10-09)


### Bug Fixes

* add python 3.14 support ([5fa1475](https://github.com/onemoola/newspy/commit/5fa147552924a5132735c1646a46b5be3bf8e30b))
* add python 3.14 support ([#401](https://github.com/onemoola/newspy/issues/401)) ([52ac22d](https://github.com/onemoola/newspy/commit/52ac22dfd2ca787c16149338119c7298a0ab4dc2))

## [2.2.15](https://github.com/onemoola/newspy/compare/v2.2.14...v2.2.15) (2025-10-05)


### Bug Fixes

* **client:** allow configurable User-Agent via environment variable ([08bcb34](https://github.com/onemoola/newspy/commit/08bcb34fb1a3558a70d8227d82ddcab98501ff84))
* **client:** allow configurable User-Agent via environment variable ([#397](https://github.com/onemoola/newspy/issues/397)) ([e9281b3](https://github.com/onemoola/newspy/commit/e9281b3a016e9c2d790a376281f51ef01d6c568f))

## [2.2.14](https://github.com/onemoola/newspy/compare/v2.2.13...v2.2.14) (2025-10-05)


### Bug Fixes

* **client:** set User-Agent header for HTTP requests in client ([cd927c7](https://github.com/onemoola/newspy/commit/cd927c77052b35dfefea93dd8a4573a3bff47274))
* **client:** set User-Agent header for HTTP requests in client ([#395](https://github.com/onemoola/newspy/issues/395)) ([e390223](https://github.com/onemoola/newspy/commit/e3902238f3afc01f4da88b7e3df088423dd17da6))
* **client:** use default User-Agent constant for HTTP requests ([9ad3c25](https://github.com/onemoola/newspy/commit/9ad3c2504ab69c55633631cbf80629857421c09b))

## [2.2.13](https://github.com/onemoola/newspy/compare/v2.2.12...v2.2.13) (2025-10-05)


### Bug Fixes

* **client:** enhance response handling in get_articles for string and None types ([a0d0994](https://github.com/onemoola/newspy/commit/a0d0994565b752686aefbc1104793f262d963a82))
* **client:** improve error handling in get_articles and support additional XML content types ([74bcb00](https://github.com/onemoola/newspy/commit/74bcb00958704279a119c82acd5686393313e127))
* **tests:** add type ignore for invalid file path in get_sources tests ([2bdc273](https://github.com/onemoola/newspy/commit/2bdc27391336efc53926bfd79469cf84dbe8e0d8))
* **tests:** add type ignore for invalid file path in get_sources tests ([#394](https://github.com/onemoola/newspy/issues/394)) ([9f71d92](https://github.com/onemoola/newspy/commit/9f71d92737c62b5e8f8bba03bba289fa4e480b14))

## [2.2.12](https://github.com/onemoola/newspy/compare/v2.2.11...v2.2.12) (2025-10-04)


### Bug Fixes

* **client:** add error handling for conflicting country and sources attributes ([b700671](https://github.com/onemoola/newspy/commit/b700671f7a75dcb87b5f4d02d01026f71a569e34))
* **client:** remove Content-Type header from RSS feed requests ([b75aaec](https://github.com/onemoola/newspy/commit/b75aaec9f59506d4e6ef7f947aad7adca06fea4c))
* **client:** remove Content-Type header from RSS feed requests ([1d6cb4e](https://github.com/onemoola/newspy/commit/1d6cb4e9ba97ab3e87cc0e6f8b3576541c969c32))
* **exceptions:** use CaseInsensitiveDict for headers in custom exception ([3265623](https://github.com/onemoola/newspy/commit/3265623ced5bce5a2b4fd3803dc435b86d2815e5))
* **http_client:** update error message to use request.url instead of request.path_url ([e2fc3aa](https://github.com/onemoola/newspy/commit/e2fc3aab20ea3a9e54a6f5a4869a6112ba4f59cb))

## [2.2.11](https://github.com/onemoola/newspy/compare/v2.2.10...v2.2.11) (2025-09-08)


### Bug Fixes

* **deps:** bump to latest versions ([8951d1c](https://github.com/onemoola/newspy/commit/8951d1c7e851b7be9b064e211787bbc37424b76b))

## [2.2.10](https://github.com/onemoola/newspy/compare/v2.2.9...v2.2.10) (2025-08-10)


### Bug Fixes

* **deps:** update poetry.lock to bump package versions ([553f9e2](https://github.com/onemoola/newspy/commit/553f9e211015661d6b0f6f800248370ed604670d))
* **deps:** update poetry.lock to bump package versions ([#357](https://github.com/onemoola/newspy/issues/357)) ([da95377](https://github.com/onemoola/newspy/commit/da95377417a9a60ce5ec6fb888fbea7a09f244db))

## [2.2.9](https://github.com/onemoola/newspy/compare/v2.2.8...v2.2.9) (2024-11-10)


### Bug Fixes

* **workflow:** revert release workflow. bump up version before build … ([#274](https://github.com/onemoola/newspy/issues/274)) ([f1796f5](https://github.com/onemoola/newspy/commit/f1796f55cfed63e129511e51b62c0ac13bce1315))
* **workflow:** revert release workflow. bump up version before build and publish step ([24aa53f](https://github.com/onemoola/newspy/commit/24aa53f224c3fbf17f604fc052e1519532c8d150))

## [2.2.8](https://github.com/onemoola/newspy/compare/v2.2.7...v2.2.8) (2024-11-10)


### Bug Fixes

* **workflow:** do not modify and commit the toml version, publish wit… ([#272](https://github.com/onemoola/newspy/issues/272)) ([58caccf](https://github.com/onemoola/newspy/commit/58caccf45689e57ab5dca3b666416f022834a6ce))
* **workflow:** do not modify and commit the toml version, publish with the version ([1655aeb](https://github.com/onemoola/newspy/commit/1655aeb0eeca161bd7d8e4a78685f03c80ae33ec))

## [2.2.7](https://github.com/onemoola/newspy/compare/v2.2.6...v2.2.7) (2024-11-10)


### Bug Fixes

* **workflow:** specify the release branch on the release workflow ([d664c8f](https://github.com/onemoola/newspy/commit/d664c8fd95d51e0fbbbfb209ca93bf4f47e54e8e))
* **workflow:** specify the release branch on the release workflow ([#271](https://github.com/onemoola/newspy/issues/271)) ([48467a7](https://github.com/onemoola/newspy/commit/48467a79d2c76e10b8c408540d47a9fcd87c8dcd))

## [2.2.6](https://github.com/onemoola/newspy/compare/v2.2.5...v2.2.6) (2024-11-10)


### Bug Fixes

* release off the release branch ([35cf7ff](https://github.com/onemoola/newspy/commit/35cf7ff08503fcf1ec68b970fd0b4c2a5642507b))
* release off the release branch ([#264](https://github.com/onemoola/newspy/issues/264)) ([2f268c5](https://github.com/onemoola/newspy/commit/2f268c52f0fa7ed08390a06bf46eeda912590e15))

## [2.2.5](https://github.com/onemoola/newspy/compare/v2.2.4...v2.2.5) (2023-09-20)


### Bug Fixes

* add more investing.com sources ([633ba4f](https://github.com/onemoola/newspy/commit/633ba4f01c49d043d34b6be542c35dc0bd3db212))
* add more investing.com sources ([#70](https://github.com/onemoola/newspy/issues/70)) ([a20001d](https://github.com/onemoola/newspy/commit/a20001d28db87f0b015dd278d2f7aae11f087603))

## [2.2.4](https://github.com/onemoola/newspy/compare/v2.2.3...v2.2.4) (2023-09-03)


### Bug Fixes

* stringify the source model ([820917c](https://github.com/onemoola/newspy/commit/820917c21d734d2e449d0fde469add76f45812f0))

## [2.2.3](https://github.com/onemoola/newspy/compare/v2.2.2...v2.2.3) (2023-09-03)


### Bug Fixes

* hide shared module ([c82b4f2](https://github.com/onemoola/newspy/commit/c82b4f2dda4a2f6027945c919d70c1c8fc0fdc38))
* move the models outside shared ([0f49e68](https://github.com/onemoola/newspy/commit/0f49e68645c90aa5a03b8c1aadc9e2f229651227))

## [2.2.2](https://github.com/onemoola/newspy/compare/v2.2.1...v2.2.2) (2023-09-03)


### Bug Fixes

* use the shared category for all ([38282ea](https://github.com/onemoola/newspy/commit/38282ea72b0826b52e170d538d26005fc8b5132e))

## [2.2.1](https://github.com/onemoola/newspy/compare/v2.2.0...v2.2.1) (2023-08-28)


### Bug Fixes

* rss source url not found ([01eacc6](https://github.com/onemoola/newspy/commit/01eacc6a371c0399eec9a0189af2f927950651ad))

# [2.2.0](https://github.com/onemoola/newspy/compare/v2.1.0...v2.2.0) (2023-08-27)


### Bug Fixes

* make the newsorg top headlines require either text, country, category and language ([db6e8d7](https://github.com/onemoola/newspy/commit/db6e8d718fa3e676cdff141ded41ae0ee1ae733c))
* make the newsorg top headlines require either text, country, category and language ([3628c2d](https://github.com/onemoola/newspy/commit/3628c2d26ea820a3b65766a99d925fc37b54708c))
* make the newsorg top headlines require either text, country, category and language ([6c48a06](https://github.com/onemoola/newspy/commit/6c48a0644f127688ef3a2837acb98b9a0757c9db))
* make the newsorg top headlines require either text, country, category and language ([4a9c7c8](https://github.com/onemoola/newspy/commit/4a9c7c8d12a698cad6562f8a1ebff7beb8bf4dce))
* make the newsorg top headlines require either text, country, category and language ([8011d8b](https://github.com/onemoola/newspy/commit/8011d8b55591fe5abe02fbe3a2b821eaade79587))


### Features

* add country and language params ([48abcc6](https://github.com/onemoola/newspy/commit/48abcc684c94d7a993d0f9e669c48e7dbb9f3936))

# [2.1.0](https://github.com/onemoola/newspy/compare/v2.0.2...v2.1.0) (2023-08-13)


### Features

* add most newsorg params ([0a2a506](https://github.com/onemoola/newspy/commit/0a2a506721b7cba7ad05dd4f131e39d9b737c7b7))
* add the default client for sources and articles ([a7c92f2](https://github.com/onemoola/newspy/commit/a7c92f22a09bc1df4bb5cd2b5684e6cb057d553f))

## [2.0.2](https://github.com/onemoola/newspy/compare/v2.0.1...v2.0.2) (2023-08-12)


### Bug Fixes

* convert to bytes and url to raw ([bfeecc1](https://github.com/onemoola/newspy/commit/bfeecc16dfb5be3cf663d106c8934d15b790e50e))

## [2.0.1](https://github.com/onemoola/newspy/compare/v2.0.0...v2.0.1) (2023-08-12)


### Bug Fixes

* compress and get the data source from remote ([3a4b617](https://github.com/onemoola/newspy/commit/3a4b6176a39c7f613bc2005d3035b194af8b9877))

# [2.0.0](https://github.com/onemoola/newspy/compare/v1.2.1...v2.0.0) (2023-08-10)


### Code Refactoring

* make it easier to call each client ([0d6b5dd](https://github.com/onemoola/newspy/commit/0d6b5dd8949a189589d761e6c8ca1741b081c443))


### Features

* add rss feed client ([0319975](https://github.com/onemoola/newspy/commit/03199752fa0fa8a6f91ac8b71feeeb6038a9a291))


### BREAKING CHANGES

* removes need for class

## [1.2.1](https://github.com/msotho/newspy/compare/v1.2.0...v1.2.1) (2023-07-07)


### Bug Fixes

* default the top headlines to business category ([2e63406](https://github.com/msotho/newspy/commit/2e63406cd37d8f65f6cd42edd80cd192ad31e271))

# [1.2.0](https://github.com/msotho/newspy/compare/v1.1.2...v1.2.0) (2023-04-07)


### Features

* add parser for xml ([c42e8d5](https://github.com/msotho/newspy/commit/c42e8d5766d3f37f8532a37041592118079f6deb))

## [1.1.2](https://github.com/msotho/newspy/compare/v1.1.1...v1.1.2) (2023-01-18)


### Bug Fixes

* remove the dependency on the python-slugify ([8b9d38d](https://github.com/msotho/newspy/commit/8b9d38d579a86dc5dae17c45f433cf25eecd1957))
* remove the dependency on the urllib3 library and use the retry from the requests library ([508bec3](https://github.com/msotho/newspy/commit/508bec315586c4bbbf2434d84d0639236dcc8136))

## [1.1.1](https://github.com/msotho/newspy/compare/v1.1.0...v1.1.1) (2023-01-03)


### Bug Fixes

* **workflow:** correct the release github actions workflow ([3a0e033](https://github.com/msotho/newspy/commit/3a0e033f4042e5bf8f424b351a64dab460438b9f))

# [1.1.0](https://github.com/msotho/newspy/compare/v1.0.0...v1.1.0) (2023-01-03)


### Features

* add the initial structure for the rss feeds ([727ced6](https://github.com/msotho/newspy/commit/727ced644ea10c08bbeff0f8f1bc0ca4dbef4b50))
* add the initial structure for the rss feeds ([cbabd39](https://github.com/msotho/newspy/commit/cbabd39199ac2c64494814fbdc636d4305d85942))
* add the initial structure for the rss feeds ([15e23c8](https://github.com/msotho/newspy/commit/15e23c8c6e949c93e48a157dfb3cf97da15b2876))

# 1.0.0 (2022-11-05)


### Features

* add the newapi client ([b86f856](https://github.com/msotho/newspy/commit/b86f8567b0eb632a81e279410f10a51353886fef))
