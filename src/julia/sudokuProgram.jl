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
        rendering = scpy.imread(fname)
        return rendering
end

global IMAGE_COUNTER = 0
OBSERVATIONS=Dict()
#OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/2edge/20141226_183342.jpg"
OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/c1.jpg"
OBS_IMAGE = scpy.imread(OBS_FNAME)
#OBS_IMAGE = int(scpy.imread(OBS_FNAME,true))/255.0
#OBS_IMAGE = edge.canny(OBS_IMAGE, sigma=1.0)
#calculate and store distance transform 
dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_IMAGE)
OBSERVATIONS["dist_obs"] = dist_obs

#CMDSB = ""
CMDSB = "4.354336037515395_4.160616090345071_17.928291145123787_4.451106998196445_5.263065771966451_0"

function PROGRAM()	
  
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)
	
	

	CMDS = Dict()
	cnt=1;
  
  ex = Uniform(4,5,1,1) 
  ey = Uniform(5,6,1,1) 
  ez = Uniform(16,19,1,1) 
  cx = Uniform(4,5,1,1) 
  cy = Uniform(4,6,1,1) 
  cz = 0
  CMDS = string(ex) * "_" * string(ey) * "_" * string(ez) * "_" * string(cx) * "_" * string(cy) * "_" * string(cz)
  CMDSB = CMDS
  
	rendering = render(CMDS)
    
	#edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering)  
  edgemap = edge.canny(rendering, sigma=1.0)
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/c",string(IMAGE_COUNTER),".png",), edgemap)
  
  
  
	#calculate distance transform
	# dist_obs = scp_morph.distance_transform_edt(~OBSERVATIONS["IMAGE"])
	valid_indxs = pyeval("npwhere(edgemap>0)", npwhere=np.where,edgemap=edgemap)
	#valid_indxs = np.where(edgemap > 0)
  
	D = pyeval("npmultiply(dist_obs[valid_indxs], ren[valid_indxs])",npmultiply=np.multiply, dist_obs=OBSERVATIONS["dist_obs"],valid_indxs=valid_indxs, ren=edgemap)

	#constraint to observation
	observe(0,Normal(0,0.35),D)

  
	return rendering
end

function PROGRAM2()	
  
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)
	
	

	CMDS = Dict()
	cnt=1;
  
  s00 = DiscreteUniform(0,9,1,1)
  s01 = -1 #DiscreteUniform(0,9,1,1)
  s02 = DiscreteUniform(0,9,1,1)
  s03 = DiscreteUniform(0,9,1,1)
  s04 = DiscreteUniform(0,9,1,1)
  s05 = -1 #DiscreteUniform(0,9,1,1)
  s06 = -1 #DiscreteUniform(0,9,1,1)
  s07 = -1 #DiscreteUniform(0,9,1,1)
  s08 = -1 #DiscreteUniform(0,9,1,1)
  s10 = -1 #DiscreteUniform(0,9,1,1)
  s11 = -1 #DiscreteUniform(0,9,1,1)
  s12 = -1 #DiscreteUniform(0,9,1,1)
  s13 = -1 #DiscreteUniform(0,9,1,1)
  s14 = -1 #DiscreteUniform(0,9,1,1)
  s15 = -1 #DiscreteUniform(0,9,1,1)
  s16 = -1 #DiscreteUniform(0,9,1,1)
  s17 = DiscreteUniform(0,9,1,1)
  s18 = DiscreteUniform(0,9,1,1)
  s20 = -1 #DiscreteUniform(0,9,1,1)
  s21 = -1 #DiscreteUniform(0,9,1,1)
  s22 = -1 #DiscreteUniform(0,9,1,1)
  s23 = -1 #DiscreteUniform(0,9,1,1)
  s24 = DiscreteUniform(0,9,1,1)
  s25 = -1 #DiscreteUniform(0,9,1,1)
  s26 = -1 #DiscreteUniform(0,9,1,1)
  s27 = -1 #DiscreteUniform(0,9,1,1)
  s28 = DiscreteUniform(0,9,1,1)
  s30 = -1 #DiscreteUniform(0,9,1,1)
  s31 = DiscreteUniform(0,9,1,1)
  s32 = -1 #DiscreteUniform(0,9,1,1)
  s33 = -1 #DiscreteUniform(0,9,1,1)
  s34 = -1 #DiscreteUniform(0,9,1,1)
  s35 = DiscreteUniform(0,9,1,1)
  s36 = -1 #DiscreteUniform(0,9,1,1)
  s37 = -1 #DiscreteUniform(0,9,1,1)
  s38 = DiscreteUniform(0,9,1,1)
  s40 = DiscreteUniform(0,9,1,1)
  s41 = DiscreteUniform(0,9,1,1)
  s42 = -1 #DiscreteUniform(0,9,1,1)
  s43 = -1 #DiscreteUniform(0,9,1,1)
  s44 = -1 #DiscreteUniform(0,9,1,1)
  s45 = -1 #DiscreteUniform(0,9,1,1)
  s46 = -1 #DiscreteUniform(0,9,1,1)
  s47 = DiscreteUniform(0,9,1,1)
  s48 = DiscreteUniform(0,9,1,1)
  s50 = DiscreteUniform(0,9,1,1)
  s51 = -1 #DiscreteUniform(0,9,1,1)
  s52 = -1 #DiscreteUniform(0,9,1,1)
  s53 = DiscreteUniform(0,9,1,1)
  s54 = -1 #DiscreteUniform(0,9,1,1)
  s55 = -1 #DiscreteUniform(0,9,1,1)
  s56 = -1 #DiscreteUniform(0,9,1,1)
  s57 = DiscreteUniform(0,9,1,1)
  s58 = -1 #DiscreteUniform(0,9,1,1)
  s60 = DiscreteUniform(0,9,1,1)
  s61 = -1 #DiscreteUniform(0,9,1,1)
  s62 = -1 #DiscreteUniform(0,9,1,1)
  s63 = -1 #DiscreteUniform(0,9,1,1)
  s64 = DiscreteUniform(0,9,1,1)
  s65 = -1 #DiscreteUniform(0,9,1,1)
  s66 = -1 #DiscreteUniform(0,9,1,1)
  s67 = -1 #DiscreteUniform(0,9,1,1)
  s68 = -1 #DiscreteUniform(0,9,1,1)
  s70 = DiscreteUniform(0,9,1,1)
  s71 = DiscreteUniform(0,9,1,1)
  s72 = -1 #DiscreteUniform(0,9,1,1)
  s73 = -1 #DiscreteUniform(0,9,1,1)
  s74 = -1 #DiscreteUniform(0,9,1,1)
  s75 = -1 #DiscreteUniform(0,9,1,1)
  s76 = -1 #DiscreteUniform(0,9,1,1)
  s77 = -1 #DiscreteUniform(0,9,1,1)
  s78 = -1 #DiscreteUniform(0,9,1,1)
  s80 = -1 #DiscreteUniform(0,9,1,1)
  s81 = -1 #DiscreteUniform(0,9,1,1)
  s82 = -1 #DiscreteUniform(0,9,1,1)
  s83 = -1 #DiscreteUniform(0,9,1,1)
  s84 = DiscreteUniform(0,9,1,1)
  s85 = DiscreteUniform(0,9,1,1)
  s86 = DiscreteUniform(0,9,1,1)
  s87 = -1 #DiscreteUniform(0,9,1,1)
  s88 = DiscreteUniform(0,9,1,1)
  
  CMDS = CMDSB * "_" 
  CMDS = CMDS * string(s00) * string(s01) * string(s02) * string(s03) * string(s04) * string(s05) * string(s06) * string(s07) * string(s08)
  CMDS = CMDS * string(s10) * string(s11) * string(s12) * string(s13) * string(s14) * string(s15) * string(s16) * string(s17) * string(s18)
  CMDS = CMDS * string(s20) * string(s21) * string(s22) * string(s23) * string(s24) * string(s25) * string(s26) * string(s27) * string(s28)
  CMDS = CMDS * string(s30) * string(s31) * string(s32) * string(s33) * string(s34) * string(s35) * string(s36) * string(s37) * string(s38)
  CMDS = CMDS * string(s40) * string(s41) * string(s42) * string(s43) * string(s44) * string(s45) * string(s46) * string(s47) * string(s48)
  CMDS = CMDS * string(s50) * string(s51) * string(s52) * string(s53) * string(s54) * string(s55) * string(s56) * string(s57) * string(s58)
  CMDS = CMDS * string(s60) * string(s61) * string(s62) * string(s63) * string(s64) * string(s65) * string(s66) * string(s67) * string(s68)
  CMDS = CMDS * string(s70) * string(s71) * string(s72) * string(s73) * string(s74) * string(s75) * string(s76) * string(s77) * string(s78)
  CMDS = CMDS * string(s80) * string(s81) * string(s82) * string(s83) * string(s84) * string(s85) * string(s86) * string(s87) * string(s88)
  
  
	rendering = render(CMDS)
    
	#edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering)  
  edgemap = edge.canny(rendering, sigma=1.0)
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/c",string(IMAGE_COUNTER),".png",), edgemap)
  
  
  
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
	scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/",string(IMAGE_COUNTER),".png",), TRACE["PROGRAM_OUTPUT"])
	IMAGE_COUNTER += 1
end

println("Start")
#load_program(PROGRAM)
#load_observations(OBSERVATIONS)
#init()
#infer(debug_callback,300,"CYCLE")
println("Finish")
println("Start")
load_program(PROGRAM2)
load_observations(OBSERVATIONS)
init()
infer(debug_callback,150,"CYCLE")
println("Finish")
# plt.show(block=true)


