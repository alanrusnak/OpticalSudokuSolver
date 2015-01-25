"""
* Copyright (c) 2014, Tejas D Kulkarni.
* 
* This file is part of Picture.
*
* Description: Picture program for 3D human pose estimation
* 
* Picture is free software: you can redistribute it and/or modify
* it under the terms of the GNU General Public License as published by
* the Free Software Foundation, either version 3 of the License, or
* (at your option) any later version.
* 
* Picture is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License along with Picture.  If not, see <http://www.gnu.org/licenses/>.
"""

include("picture.jl")
using Debug
@pyimport scipy.misc as scpy
@pyimport skimage.filter as edge
@pyimport scipy.ndimage.morphology as scp_morph
@pyimport numpy as np
################### PROBABILISTIC CODE ###############


@debug function render(CMDS)
	      client = connect(5005)
        println(client,CMDS)
        fname = readline(client)
        fname = strip(fname)
        close(client)
        rendering = scpy.imread(str)
        return rendering
end

global IMAGE_COUNTER = 0
OBSERVATIONS=Dict()
OBS_FNAME = "C:/Users/Alan/Documents/Project/20141224_143900.jpg"
OBS_IMAGE = int(scpy.imread(OBS_FNAME,true))/255.0
OBS_IMAGE = edge.canny(OBS_IMAGE, sigma=1.0)
#calculate and store distance transform 
dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_IMAGE)
OBSERVATIONS["dist_obs"] = dist_obs


function PROGRAM()	
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)
	
	

	CMDS = Dict()
	cnt=1;

  ex = 2
  ey = 4.4
  ez = 18
  cx = 4.5
  cy = 4.5
  cz = 0
  CMDS = string(ex) * "_" * string(ey) * "_" * string(ez) * "_" * string(cx) * "_" * string(cy) * "_" * string(cz)  

	rendering = render(CMDS)

	edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering) #edgemap = edge.canny(rendering, sigma=1.0)

	#calculate distance transform
	# dist_obs = scp_morph.distance_transform_edt(~OBSERVATIONS["IMAGE"])
	valid_indxs = pyeval("npwhere(edgemap>0)", npwhere=np.where,edgemap=edgemap)
	#valid_indxs = np.where(edgemap > 0)
	D = pyeval("npmultiply(dist_obs[valid_indxs], ren[valid_indxs])",npmultiply=np.multiply, dist_obs=OBSERVATIONS["dist_obs"],valid_indxs=valid_indxs, ren=edgemap)

	#constraint to observation
	observe(0,Normal(0,0.35),D)

	return rendering
end

########### USER DIAGNOSTICS ##############
# plt.ion()
function debug_callback(TRACE)
	global IMAGE_COUNTER
	println("LOGL=>", TRACE["ll"])
	scpy.imsave(string("C:/Users/Alan/Documents/Project/output/",string(IMAGE_COUNTER),".png",), TRACE["PROGRAM_OUTPUT"])
	IMAGE_COUNTER += 1
end

load_program(PROGRAM)
load_observations(OBSERVATIONS)
init()
infer(debug_callback,10,"CYCLE")

# plt.show(block=true)


