"""Per-workflow replacement for the --disable-comfy-compiler launch flag.

ComfyUI reads `args.disable_comfy_compiler` / `args.disable_cuda_graphs` at call time
(comfy/model_prefetch.py: malloc_graph_enabled / prefetch_queue_pop), so we flip them only
while the patched model's diffusion forward runs, then restore them.
"""
from comfy.cli_args import args


class DisableComfyCompiler:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "model": ("MODEL",),
                "disable": ("BOOLEAN", {"default": True}),
            }
        }

    RETURN_TYPES = ("MODEL",)
    FUNCTION = "patch"
    CATEGORY = "advanced/model"

    def patch(self, model, disable=True):
        if not disable:
            return (model,)

        m = model.clone()
        previous = m.model_options.get("model_function_wrapper")

        def wrapper(apply_model, wrapper_args):
            old = (args.disable_comfy_compiler, args.disable_cuda_graphs)
            args.disable_comfy_compiler = True
            args.disable_cuda_graphs = True
            try:
                if previous is not None:
                    return previous(apply_model, wrapper_args)
                return apply_model(wrapper_args["input"], wrapper_args["timestep"], **wrapper_args["c"])
            finally:
                args.disable_comfy_compiler, args.disable_cuda_graphs = old

        m.set_model_unet_function_wrapper(wrapper)
        return (m,)


NODE_CLASS_MAPPINGS = {"DisableComfyCompiler": DisableComfyCompiler}
NODE_DISPLAY_NAME_MAPPINGS = {"DisableComfyCompiler": "Disable Comfy Compiler"}
