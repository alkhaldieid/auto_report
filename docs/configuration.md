# Configuration

Auto Report loads YAML, TOML, or JSON configuration and merges it over a built-in preset.

## Presets

- `arabic-facility`: default preset that preserves the original Arabic daily/monthly facility-management workflow.
- `general`: neutral LTR preset for custom organizations.

Use a preset directly:

```bash
auto-report --preset general generic ./report-folder --tex-only
```

Or select one inside `report.yml`:

```yaml
preset: general
```

## Top-Level Fields

- `direction`: `ltr` or `rtl`.
- `font_name`: font passed to XeLaTeX `fontspec`.
- `font_options`: optional `fontspec` options such as `Script=Arabic`.
- `contents_name`: table-of-contents label.
- `figure_name`: figure label.
- `image_caption_template`: fallback caption template. Supports `{section_title}`, `{section_folder}`, and `{mode}`.
- `image_extensions`: supported image suffixes.
- `output_dir`: output directory relative to the input report folder.
- `title_page`: title page content and optional assets.
- `modes`: mode-specific title, subtitle, and output filename templates.
- `sections`: ordered list of image folders to include.

## Template Variables

Mode and title-page strings can use:

- `{input_name}`: input folder name.
- `{mode}`: active mode.
- `{mode_title}`: resolved mode title.
- `{mode_subtitle}`: resolved mode subtitle.
- `{date_ar}`: Arabic date parsed from daily folders such as `9-9-2030`.
- `{date_en}`: English date parsed from daily folders.
- `{period_label}`: month label inferred from folders such as `09-2030`; otherwise the folder name.

## Example YAML

See [report.yml](report.yml):

```yaml
preset: general
direction: ltr
font_name: "Latin Modern Roman"
output_dir: reports

title_page:
  enabled: true
  title: "{mode_title}"
  subtitle: "{mode_subtitle}"
  logo_path: assets/logo.png
  cover_path: assets/cover.jpg

modes:
  generic:
    title: "Project Photo Report"
    subtitle: "North Site Inspection"
    output_filename: "north-site-photo-report"

sections:
  - folder: before
    title: Before Photos
  - folder: after
    title: After Photos
```

Relative logo, cover, section, and output paths are resolved from the report input folder.
