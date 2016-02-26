---
title: "D3/SVG drawing in Absolute Units"
layout: post
date:   2014-05-08
---

# {{ page.title }}

### Update, 2014-07-30:

[iPipet](http://ipipet.teamerlich.org/) is published, see
[Blog Post](http://erlichya.tumblr.com/post/93339535499/ipipet-a-creative-hack-born-out-of-necessity),
[Press Release](http://wi.mit.edu/news/archive/2014/innovative-scientists-update-old-school-pipetting-new-age-technology),
[Bio-IT world story](http://www.bio-itworld.com/2014/7/30/pad-pipetter-eases-tedious-lab-work.html),
[Nature Methods Correspondence](http://www.nature.com/nmeth/journal/v11/n8/full/nmeth.3028.html).

## Background

To create [iPipet](http://ipipet.teamerlich.org/) we needed a simple method to draw
shapes in absolute units - that is, have a known physical size in the real world -
so that our plate template would align perfectly on the iPad screen with a
[96-Well Plate](http://en.wikipedia.org/wiki/Microtiter_plate).

![](./images/ipipet_top_350.jpg)  ![](./images/ipipet_side_350.jpg)

Absolute units work very well in printed documents,
but are [not recommended](http://www.w3.org/Style/Examples/007/units.en.html)
when displaying documents on screen (ie. computer monitors).
Too many technical factors prevent accurate rendering of absolute units on common screens.

However, when using well-characterized devices whose display resolution is
known (e.g iPads), drawing with absolute units is relateively easy.

## Screen Resolution on Known Devices

The diameter of this green circle will be 1/2-inch *only* on specific computer monitors:

<svg id="greencircle1" style="vertical-align:middle;" viewBox="0 0 0.5 0.5" width="48" height="48">
  <circle cx="0.25" cy="0.25" r="0.25" style="fill:green"/>
</svg><span>&larr; Exactly half-inch green circle, if your display's resolution is 96dpi</span>


When designing a website for a specific device, the display resolution is usually known
in advance.
Wikipedia has a list of [display densities](http://en.wikipedia.org/wiki/List_of_displays_by_pixel_density).
In theory, if a display resolution for a device is 132ppi (pixels-per-inch,
also known as DPI, dots-per-inch) drawing 132 pixels-long line on the screen will
measure exactly 1 inch.

When using HTML/CSS/SVG, we must account for an additional factor: **CSS Pixel Ratio**.

One of these red bars will be exactly 1-inch wide, if your display's resolution
matches <i>and</i> your device's CSS pixel ratio is 1:
<div>
    <div style="background-color:red;text-align:right;width:96px;">96 pixels</div>
    <div style="background-color:red;text-align:right;width:104px;">104 pixels</div>
    <div style="background-color:red;text-align:right;width:128px;">128 pixels</div>
    <div style="background-color:red;text-align:right;width:132px;">132 pixels</div>
    <div style="background-color:red;text-align:right;width:153px;">153 pixels</div>
    <div style="background-color:red;text-align:right;width:200px;">200 pixels</div>
</div>

*CSS Pixel Ratio** enables devices to scale web-pages to a size easily readable
by users. It must be taken into account when rendering absolute units.
CSS Media Queries trickery can sometimes be used to automatically detect the device's
density and CSS-pixel ratio. Often, it's easier to ask the user which device is being used
(or detect it automatically) and consult wikipedia's list of known device densities
(See 'Further Information' below for references).

## Using absolute units with SVG

SVG's [ViewBox](http://www.w3.org/TR/SVG11/coords.html#ViewBoxAttribute)
attribute is used to specify to logical units inside of the SVG elements. The
syntax is `viewBox = <min-x> <min-y> <width> <height>`. Here, `<width>` and
`<height>` represent the logical left-most and bottom-most positions of the elements
*inside* the SVG. For brevity, we'll treat the `viewBox` coordinates as logical,
absolute units.

Example: The following SVG will be a square measuring 1-by-1 logical units,
and inside it, a 0.5-by-0.5 green square and 1-by-0.25 blue rectangle.
**Note:** The size (in pixels) of the SVG element was not defined, so the logical
unit size of 1 *does not* yet correspond to any known size on the device.


    <svg id="my_svg" viewBox="0 0 1 1">
      <rect x="0" y=0"    width="0.5" height="0.5"  fill="green"></rect>
      <rect x="0" y="0.5" width="1"   height="0.25" fill="blue"></rect>
    </svg>

<svg id="my_svg" viewBox="0 0 1 1">
  <rect x="0" y=0"    width="0.5" height="0.5"  fill="green"></rect>
  <rect x="0" y="0.5" width="1"   height="0.25" fill="blue"></rect>
</svg>

Next, we'll specify the size (in pixels) of the SVG element, based on the device
display density and CSS Pixel ratio. Since we've used logical SVG size of 1-by-1,
and we want the SVG to measure exactly 1-inch, the pixel size of the SVG element
should be the device density itself (i.e. If the device's display density is
132 pixels-per-inch, and we want to display 1-inch, the width and height of the SVG
element should be exactly 132 pixels. This assumes CSS pixel ratio of 1).

Example: on a 1st/2nd generation iPad with display resolution of 132ppi, the
following SVG will measure exacly 1-inch (the green square will measure 0.5-by-0.5 inch,
the blue rectangle will measure 1-by-0.25 inch):

    <svg id="my_svg" viewBox="0 0 1 1" width="132px" height="132px">
      <rect x="0" y=0"    width="0.5" height="0.5"  fill="green"></rect>
      <rect x="0" y="0.5" width="1"   height="0.25" fill="blue"></rect>
    </svg>

<svg style="vertical-align:top;" id="my_svg1" viewBox="0 0 1 1" width="132px" height="132px">
  <rect x="0" y=0"    width="0.5" height="0.5"  fill="green"></rect>
  <rect x="0" y="0.5" width="1"   height="0.25" fill="blue"></rect>
</svg><span>&larr; Exactly half-inch green square on iPad 1/2 (132ppi)</span>


Click here for a [Demo of SVG absolute units for multiple devices](./examples/svg_units.html).

## Absolute Units with D3

[D3 (Data-Driven Documents)](http://d3js.org/) is a Javascript library for
manipulating documents based on data. Internally, D3 uses SVG. The same principles
apply to D3 when rendering absolute units, except with D3, the measurements
are usually entered programatically:


    <div id="drawing"></div>

    <script>
    /* Determine proper values at runtime, when the page loads on the device */
    var device_width_ppi  = 96 ;
    var device_height_ppi = 96 ;

    /* Desired size in absolute units */
    var desired_width_inches = 1 ;
    var desired_height_inches = 1 ;
    var viewBox = "0 0 " + desired_width_inches + " " + desired_height_inches ;

    /* Data/Elements to draw. Units are LOGICAL (inches) */
    var items = [
      { "x": 0,  "y":0,   "w":0.5,   "h":0.5,  "fill":"green" },
      { "x": 0,  "y":0.5, "w":1.0,   "h":0.25, "fill":"blue"  }
      ];

    var svg = d3.select("#drawing").append("svg")
      .attr("id","my_svg")
      .attr("viewBox", viewBox)
      .attr("width",  device_width_ppi  * desired_width_inches)
      .attr("height", device_height_ppi * desired_height_inches);

    svg.selectAll(".item")
       .data(items)
     .enter().append("rect")
       .attr("class","item")
       .attr("x",     function(d) { return d.x; } )
       .attr("y",     function(d) { return d.y; } )
       .attr("width", function(d) { return d.w; } )
       .attr("height",function(d) { return d.h; } )
       .attr("fill",  function(d) { return d.fill; } );

    </script>


Click here for a [Demo of D3 drawing with absolute units](./examples/d3_units.html).

## Changing Resolution Dynamically

The following javascript/JQuery code can be used to change the size (in pixels) of an
existing SVG object:


    function change_resolution(new_ppi)
    {
        /* These must match the viewBox size of the SVG */
        var desired_width_inches = 1 ;
        var desired_height_inches = 1 ;

        var new_width_pixels  = new_ppi * desired_width_inches ;
        var new_height_pixels = new_ppi * desired_height_inches ;

        $("#my_svg").attr("width", new_width_pixels + "px");
        $("#my_svg").attr("height",new_height_pixels + "px");
    }


## Further Information

- [Actual Size Ruler](http://www.ginifab.com/feeds/cm_to_inch/actual_size_ruler.html)
- [W3C Web Style Sheets Tips and Tricks](http://www.w3.org/Style/Examples/007/units.en.html)
- [SVG Coordinate systems, Transformations and Units](http://www.w3.org/TR/SVG11/coords.html#ViewBoxAttribute)
- [List of Displays Densities by Manufacturers](http://en.wikipedia.org/wiki/List_of_displays_by_pixel_density)
- [A Pixel Identity Crisis (an informative review)](http://alistapart.com/article/a-pixel-identity-crisis/)
- [CSS Media Queries](https://developer.mozilla.org/en-US/docs/Web/Guide/CSS/Media_queries)
- [A Pixel is not A Pixel (about CSS Pixel Ratio)](http://www.quirksmode.org/blog/archives/2010/04/a_pixel_is_not.html)
- [Device Pixel Density Tests](http://bjango.com/articles/min-device-pixel-ratio/)
- [D3](<http://d3js.org/)
- [iPipet](http://ipipet.teamerlich.org/)

