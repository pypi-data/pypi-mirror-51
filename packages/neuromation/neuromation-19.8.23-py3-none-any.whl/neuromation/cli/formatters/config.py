from sys import platform

from click import style

from neuromation.cli.root import Root


class ConfigFormatter:
    def __call__(self, root: Root) -> str:
        if platform == "win32":
            yes, no = "Yes", "No"
        else:
            yes, no = "✔︎", "✖︎"
        lines = []
        lines.append(style("User Name", bold=True) + f": {root.username}")
        lines.append(style("API URL", bold=True) + f": {root.url}")
        lines.append(style("Docker Registry URL", bold=True) + f": {root.registry_url}")
        lines.append(style("Resource Presets", bold=True) + f":")
        indent = "  "
        lines.append(f"{indent}Name         #CPU  Memory Preemptible #GPU  GPU Model")
        for name, preset in root.resource_presets.items():
            lines.append(
                (
                    f"{indent}{name:12}  {preset.cpu:>3} {preset.memory_mb:>7} "
                    f"{yes if preset.is_preemptible else no:^11}"
                    f"  {preset.gpu or '':>3}"
                    f"  {preset.gpu_model or ''}"
                ).rstrip()
            )
        return (
            style("User Configuration", bold=True)
            + ":\n"
            + indent
            + f"\n{indent}".join(lines)
        )
