# mfisp

microfluidic image stack processing

**NOTE: Pre-alpha tools, functionality subject to change without notice!**

Some miscellaneous tools helpful for working with image stacks (with microfluidic structures). Currently contains the following utilities:

## Tools

### register

Registration routine from [molyso](https://github.com/modsim/molyso), will automatically register the input stack and possible additional channels.

```bash
> python -m mfisp.registration --output result.tif --channel 0 input.tif
```

### autorotate

Automatic rotation detection and de-rotation from [molyso](https://github.com/modsim/molyso).
(Hint: Try to have OpenCV installed for your Python version, otherwise the rotation will be *very* slow.
Windows users take a look [here](http://www.lfd.uci.edu/~gohlke/pythonlibs/#opencv).)

```bash
> python -m mfisp.autorotate --output result.tif --channel 0 input.tif
```

### boxcrop

Uses the register and autorotate functionality as described above, and [detects rectangular growth structures](https://github.com/csachs/mfisp-boxdetection) as region of interst (ROI). The resulting stack will contain only the ROI.

```bash
> python -m mfisp.boxcrop --output result.tif --channel 0 input.tif
```

## License

2-clause BSD.
