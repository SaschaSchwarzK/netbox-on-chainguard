# NetBox on Chainguard

CVE-clean NetBox Docker images built on [Chainguard Python](https://images.chainguard.dev/directory/image/python/overview).

Supports the NetBox releases listed in [`versions.json`](versions.json). Uses [granian](https://github.com/emmett-framework/granian) (WSGI/uvloop) instead of gunicorn.

## Image versions

Each image has an immutable downstream revision tag such as `4.6.8-r2` or
`4.7.2-r0`. The revision is incremented whenever that NetBox release is rebuilt
with a patched base image or dependency set. Moving convenience tags such as
`4.7.2` point to the newest revision; `latest` points to the newest configured
NetBox release.

`versions.json` is the single editable build matrix. Add a new entry at the end
when NetBox publishes a release, or remove an entry when it is no longer
supported:

```json
{"version": "4.7.3", "revision": 0}
```

Every version also has a matching file in `security-requirements/`. These
overrides replace vulnerable upstream pins while retaining the dependency
release line supported by that NetBox version.

### Released images and current vulnerabilities

This table is generated from Grype and Trivy scans of the published immutable
images. It is refreshed immediately after a release and by the nightly scan. A
clean release has no critical or high findings; medium and low findings remain
visible here and in its release notes.

<!-- released-images:start -->
| NetBox | Image | Critical | High | Medium | Low | Current vulnerabilities |
|---|---|---:|---:|---:|---:|---|
| 4.7.3 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.3-r3` | 1 | 16 | 9 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-h2r5-x5m7-3935](https://github.com/advisories/GHSA-h2r5-x5m7-3935), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.7.2 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.2-r3` | 1 | 16 | 9 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-h2r5-x5m7-3935](https://github.com/advisories/GHSA-h2r5-x5m7-3935), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.7.1 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.1-r3` | 1 | 16 | 9 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-h2r5-x5m7-3935](https://github.com/advisories/GHSA-h2r5-x5m7-3935), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.7.0 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.7.0-r3` | 1 | 16 | 9 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-h2r5-x5m7-3935](https://github.com/advisories/GHSA-h2r5-x5m7-3935), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.6.10 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.10-r3` | 1 | 16 | 8 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.6.9 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.9-r3` | 1 | 16 | 8 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
| 4.6.8 | `ghcr.io/saschaschwarzk/netbox-on-chainguard:4.6.8-r3` | 1 | 16 | 8 | 2 | [CVE-2026-114583](https://nvd.nist.gov/vuln/detail/CVE-2026-114583), [CVE-2026-115557](https://nvd.nist.gov/vuln/detail/CVE-2026-115557), [CVE-2026-14662](https://nvd.nist.gov/vuln/detail/CVE-2026-14662), [CVE-2026-14663](https://nvd.nist.gov/vuln/detail/CVE-2026-14663), [CVE-2026-14664](https://nvd.nist.gov/vuln/detail/CVE-2026-14664), [CVE-2026-14666](https://nvd.nist.gov/vuln/detail/CVE-2026-14666), [CVE-2026-14668](https://nvd.nist.gov/vuln/detail/CVE-2026-14668), [CVE-2026-14669](https://nvd.nist.gov/vuln/detail/CVE-2026-14669), [CVE-2026-14670](https://nvd.nist.gov/vuln/detail/CVE-2026-14670), [CVE-2026-14671](https://nvd.nist.gov/vuln/detail/CVE-2026-14671), [CVE-2026-14672](https://nvd.nist.gov/vuln/detail/CVE-2026-14672), [CVE-2026-14677](https://nvd.nist.gov/vuln/detail/CVE-2026-14677), [CVE-2026-14678](https://nvd.nist.gov/vuln/detail/CVE-2026-14678), [CVE-2026-14679](https://nvd.nist.gov/vuln/detail/CVE-2026-14679), [CVE-2026-14680](https://nvd.nist.gov/vuln/detail/CVE-2026-14680), [CVE-2026-14681](https://nvd.nist.gov/vuln/detail/CVE-2026-14681), [CVE-2026-15741](https://nvd.nist.gov/vuln/detail/CVE-2026-15741), [CVE-2026-15742](https://nvd.nist.gov/vuln/detail/CVE-2026-15742), [CVE-2026-16239](https://nvd.nist.gov/vuln/detail/CVE-2026-16239), [CVE-2026-16241](https://nvd.nist.gov/vuln/detail/CVE-2026-16241), [CVE-2026-18024](https://nvd.nist.gov/vuln/detail/CVE-2026-18024), [CVE-2026-18408](https://nvd.nist.gov/vuln/detail/CVE-2026-18408), [CVE-2026-19385](https://nvd.nist.gov/vuln/detail/CVE-2026-19385), [CVE-2026-6464](https://nvd.nist.gov/vuln/detail/CVE-2026-6464), [CVE-2026-6469](https://nvd.nist.gov/vuln/detail/CVE-2026-6469), [CVE-2026-6470](https://nvd.nist.gov/vuln/detail/CVE-2026-6470), [CVE-2026-6471](https://nvd.nist.gov/vuln/detail/CVE-2026-6471), [GHSA-2pm8-9426-243p](https://github.com/advisories/GHSA-2pm8-9426-243p), [GHSA-3v2h-jgrj-9jmm](https://github.com/advisories/GHSA-3v2h-jgrj-9jmm), [GHSA-4g6h-pg6m-qwgx](https://github.com/advisories/GHSA-4g6h-pg6m-qwgx), [GHSA-5qv4-w274-5rpv](https://github.com/advisories/GHSA-5qv4-w274-5rpv), [GHSA-6hh9-353p-vfvp](https://github.com/advisories/GHSA-6hh9-353p-vfvp), [GHSA-c4j6-v5f3-8f3c](https://github.com/advisories/GHSA-c4j6-v5f3-8f3c), [GHSA-fvh5-w7wg-xp3g](https://github.com/advisories/GHSA-fvh5-w7wg-xp3g), [GHSA-gfpv-wrhp-wwh6](https://github.com/advisories/GHSA-gfpv-wrhp-wwh6), [GHSA-hp2m-55fj-8mw5](https://github.com/advisories/GHSA-hp2m-55fj-8mw5), [GHSA-hv8p-f6vx-h5x6](https://github.com/advisories/GHSA-hv8p-f6vx-h5x6), [GHSA-j447-m374-x28h](https://github.com/advisories/GHSA-j447-m374-x28h), [GHSA-j586-36cw-2gc2](https://github.com/advisories/GHSA-j586-36cw-2gc2), [GHSA-jvgx-qpg4-cv6w](https://github.com/advisories/GHSA-jvgx-qpg4-cv6w), [GHSA-m27x-8754-w5v9](https://github.com/advisories/GHSA-m27x-8754-w5v9), [GHSA-m6g7-vvh9-445r](https://github.com/advisories/GHSA-m6g7-vvh9-445r), [GHSA-mpj9-cx22-xp87](https://github.com/advisories/GHSA-mpj9-cx22-xp87), [GHSA-mpm7-fx5w-5w53](https://github.com/advisories/GHSA-mpm7-fx5w-5w53), [GHSA-p6pp-53vr-h4w8](https://github.com/advisories/GHSA-p6pp-53vr-h4w8), [GHSA-p745-282f-cxpr](https://github.com/advisories/GHSA-p745-282f-cxpr), [GHSA-ph64-qjwg-mxwq](https://github.com/advisories/GHSA-ph64-qjwg-mxwq), [GHSA-r26j-h78w-pjqm](https://github.com/advisories/GHSA-r26j-h78w-pjqm), [GHSA-rvq6-xp6x-5575](https://github.com/advisories/GHSA-rvq6-xp6x-5575), [GHSA-rw5c-m5ff-2772](https://github.com/advisories/GHSA-rw5c-m5ff-2772), [GHSA-v5vg-62mg-4ccv](https://github.com/advisories/GHSA-v5vg-62mg-4ccv), [GHSA-v76f-gmv6-95jw](https://github.com/advisories/GHSA-v76f-gmv6-95jw), [GHSA-xxfm-85xf-vx5m](https://github.com/advisories/GHSA-xxfm-85xf-vx5m) |
<!-- released-images:end -->

## Build arguments

| Argument | Description | Example |
|---|---|---|
| `NETBOX_VERSION` | NetBox release version | `4.7.0` |

The Dockerfile uses `cgr.dev/chainguard/python:latest-dev` for the build stage and `cgr.dev/chainguard/python:latest` for the runtime stage (the free public images). For production, both will be referenceable via a `.baseimage.lock` file or as build arguments.

## Local build

```sh
docker buildx build \
  --build-arg NETBOX_VERSION=4.7.0 \
  -t netbox-chainguard:4.7.0 \
  --load .
```

## Local run (docker compose)

```sh
export NETBOX_VERSION=4.7.0
docker compose up -d
```

NetBox will be available at http://localhost:8080.

Default credentials (dev only — change in `env/netbox.env`): `admin` / `admin`

## Security properties

- Non-root UID 65532, GID 0 (root group, no root privileges)
- No login shell (`/sbin/nologin`)
- No package manager in final image (Chainguard distroless-style)
- Read-only filesystem at runtime (no shell, no write access outside mounted volumes)
- Chainguard base has near-zero CVEs by design
- SBOM + provenance via `docker/build-push-action`

## Configuration

Mount custom config files into `/etc/netbox/config/`. All `*.py` files in that directory are loaded automatically after `configuration.py`.

See `configuration/extra.py` for examples (plugins, custom storage backends, etc.).

---

## Differences from netbox-docker

This project is inspired by [netbox-community/netbox-docker](https://github.com/netbox-community/netbox-docker) but differs in several significant ways.

### Base image

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| Base OS | Debian (bookworm) | Chainguard Python (Wolfi/Alpine-based) |
| Build stage | `debian:bookworm-slim` | `cgr.dev/chainguard/python:latest-dev` |
| Runtime stage | `debian:bookworm-slim` | `cgr.dev/chainguard/python:latest` |
| CVE surface | Moderate (Debian packages) | Near-zero (Chainguard hardened) |
| Shell in runtime | `/bin/bash` present | No shell at all |
| Package manager in runtime | `apt` present | No package manager |

### Runtime user

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| UID | 999 (`netbox`, created at build) | 65532 (`nonroot`, pre-existing in Chainguard image) |
| GID | 0 (root group) | 0 (root group) |
| Shell | `/bin/false` | `/sbin/nologin` (Chainguard default) |
| User created at build | Yes (`useradd`) | No (already exists in base image) |

### Entrypoint and scripts

netbox-docker uses shell scripts (`docker-entrypoint.sh`, `launch-netbox.sh`, `health.sh`). This project replaces all of them with Python scripts because the Chainguard runtime image contains no shell:

| netbox-docker | netbox-on-chainguard |
|---|---|
| `docker-entrypoint.sh` (bash) | `entrypoint.py` (Python) |
| `launch-netbox.sh` (bash) | `launch.py` (Python, `os.execv`) |
| `health.sh` (bash + curl) | `health.py` (Python `urllib`) |

### Web server

Both projects use [granian](https://github.com/emmett-framework/granian) with uvloop as the WSGI server (gunicorn is removed). Configuration is identical.

### Package installation

| | netbox-docker | netbox-on-chainguard |
|---|---|---|
| Installer | `uv` (copied from `ghcr.io/astral-sh/uv`) | `uv` (pre-installed in Chainguard dev image) |
| NetBox source | Cloned/copied from local path | Downloaded from GitHub releases tarball at build time |
| `collectstatic` | Run at build time | Run at build time |

### LDAP support

netbox-docker includes `django-auth-ldap` in `requirements-container.txt`. This project **does not** — `python-ldap` (a C extension that `django-auth-ldap` depends on) cannot be built with Chainguard's cross-compilation toolchain due to a linker sysroot issue (`libldap.a` is not compiled with `-fPIC`).

LDAP authentication is an **opt-in** feature in NetBox. It is not required for any other functionality including OIDC, SAML, or SSO. Users who need LDAP must build a custom image layer on top of this one.

### Read-only filesystem and plugin requirements

**This is the most important operational difference.**

The Chainguard runtime image has no shell and no package manager. The filesystem is effectively read-only at runtime — there is no way to `pip install` anything after the image is built.

**All Python packages must be present at build time.** This includes:

- NetBox plugins
- Any Python dependencies of those plugins
- Any optional NetBox features that require additional packages (e.g. `django-auth-ldap`, custom storage backends)

Add everything to `requirements-container.txt` before building:

```txt
# requirements-container.txt
dulwich==1.2.14
granian[uvloop]==2.8.2
python3-saml==1.16.0
--no-binary lxml
--no-binary xmlsec
sentry-sdk[django]==2.69.1

# Example: add plugins and their dependencies here
# netbox-bgp==0.14.0
# netbox-topology-views==4.1.1
```

Then enable the plugin in `configuration/extra.py`:

```python
from netbox.configuration.configuration import PLUGINS, PLUGINS_CONFIG
PLUGINS.append('netbox_bgp')
PLUGINS_CONFIG['netbox_bgp'] = {}
```

Attempting to reference a plugin that is not installed in the venv will cause NetBox to fail at startup with `ImproperlyConfigured`.

### Shared library handling

The Chainguard runtime image is minimal and does not include all shared libraries that Python C extensions require. This project explicitly copies the following libraries from the build stage into the runtime image to support `psycopg[c]` (the PostgreSQL C driver):

- `libpq.so.5` — PostgreSQL client library
- `libgssapi_krb5.so.2`, `libkrb5.so.3`, `libk5crypto.so.3`, `libkrb5support.so.0` — Kerberos (required by libpq)
- `libcom_err.so.2`, `libkeyutils.so.1` — Kerberos support libs
- `libldap.so.2`, `liblber.so.2` — LDAP (required by libpq for GSSAPI)
- `libsasl2.so.3` — SASL (required by libldap)

`libssl.so.3` and `libcrypto.so.3` are already present in the Chainguard Python runtime image.

### What is intentionally omitted

Compared to netbox-docker, the following are not included and not planned:

| Feature | Reason |
|---|---|
| LDAP auth (`django-auth-ldap`) | Cannot build `python-ldap` C extension with Chainguard cross-toolchain |
| `openssh-client` | Not needed for core NetBox functionality |
| `bzip2` | Not needed |
| Debian system Python | Replaced by Chainguard's Python |
| `apt`/`apk` in runtime | Intentionally absent (security property) |
