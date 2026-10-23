# ComfyUI-DisableComfyCompiler

> [!IMPORTANT]
> **This repo has moved.** The node is now part of **[ComfyUI-RulZnodes](https://github.com/speedyrulz/ComfyUI-RulZnodes)**,
> together with the HEIC Load Image, Load Image Batch (Simple) and Mask Intelligent Crop nodes. This repo is
> archived and won't get updates.
>
> To switch, delete this folder from `custom_nodes` and install ComfyUI-RulZnodes. The node ID is unchanged,
> so existing workflows keep working.

A per-workflow replacement for the `--disable-comfy-compiler` launch flag.

The **Disable Comfy Compiler** node (`advanced/model`) takes a `MODEL` and returns a clone that
turns the Comfy model compiler (and its CUDA graph subfeature) off only while that model's
diffusion forward pass runs. The flags are restored afterwards, so other workflows are unaffected.

## Install

```bash
cd ComfyUI/custom_nodes
git clone https://github.com/speedyrulz/ComfyUI-DisableComfyCompiler
```

Restart ComfyUI (without `--disable-comfy-compiler`) and place the node between your model loader and sampler.

## Notes

- Tested on ComfyUI 0.37.0 with Qwen Image 2.1.
- Only the diffusion model is covered; text encoders and latent previews are not affected.
