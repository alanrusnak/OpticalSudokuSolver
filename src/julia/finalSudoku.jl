# Alan Rusnak, 2015, University of Cambridge

include("engine/picture.jl")
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
#OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/20141224_144544.jpg"
OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/g3.jpg"
#OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/st/20150507_224925.jpg"
OBS_IMAGE = scpy.imread(OBS_FNAME)
OBS_EDGE = int(scpy.imread(OBS_FNAME,true))/255.0
OBS_EDGE = edge.canny(OBS_IMAGE, sigma=1.0)
dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_EDGE)
OBSERVATIONS["dist_obs"] = dist_obs

#OBS_IMAGE = pyeval("canny(OBS_IMAGE,1.0)", canny = edge.canny, OBS_IMAGE=OBS_IMAGE)
#scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/obs_image3.png",), OBS_IMAGE)
#calculate and store distance transform
#global dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_EDGE)
#OBSERVATIONS["dist_obs"] = dist_obs
global CMDSB = ""
global CMDS = ""
global OBS_NAME = ""


minD = typemax(Int64)

function PROGRAM()
  global CMDS
  global CMDSB
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)


	CMDS = Dict()
	cnt=1;


  ex = Uniform(1,8,1,1)
  ey = Uniform(1,8,1,1)
  ez = Uniform(15,18,1,1)
  cx = Uniform(3,6,1,1)
  cy = Uniform(3,6,1,1)
  r = Uniform(-1,1,1,1)
  cz = 0



  CMDS = string(ex) * "_" * string(ey) * "_" * string(ez) * "_" * string(cx) * "_" * string(cy) * "_" * string(r)



	rendering = render(CMDS)




	  edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering)
  #edgemap = edge.canny(rendering, sigma=1.0)
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/c",string(IMAGE_COUNTER),".png",), edgemap)



	#calculate distance transform
	# dist_obs = scp_morph.distance_transform_edt(~OBSERVATIONS["IMAGE"])
	 valid_indxs = pyeval("npwhere(edgemap>0)", npwhere=np.where,edgemap=edgemap)
	#valid_indxs = np.where(edgemap > 0)

	  D = pyeval("npmultiply(dist_obs[valid_indxs], ren[valid_indxs])",npmultiply=np.multiply, dist_obs=OBSERVATIONS["dist_obs"],valid_indxs=valid_indxs, ren=edgemap)



  observe(0,Normal(0,0.35),D)

	return rendering
end

function PROGRAM2()
  global CMDS
  global CMDSB
  global OBS_IMAGE
  global OBS_NAME
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)



	CMDS = Dict()
	cnt=1;


  CMDS = CMDSB * "_"

  minChar = 0
  minDiff = typemax(Int64)
  avg = avgColor(OBS_IMAGE)

  for i in 1:81
    for j in 0:9
      if(j==0)
        CMDSTry = CMDS * string(j)
        rendering = render(CMDSTry)
        minDiff = pixelError(OBS_IMAGE,rendering,avg)
        minChar = j
      else
        CMDSTry = CMDS * string(j)
        rendering = render(CMDSTry)
        pError = pixelError(OBS_IMAGE,rendering,avg)
        if(pError<minDiff)
          minDiff = pError
          minChar = j
        end
      end
    end
    #println(i)
    CMDS = CMDS * string(minChar)
    minDiff = typemax(Int64)
  end

  rendering = render(CMDS)
  scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output2/" * CMDS * ".png",), rendering)
  #println(CMDS)

	return rendering
end

  #OBS_FNAME3 = "C:/Users/Alan/Documents/SudokuProject/diff10.png"
  #OBS_IMAGE3 = scpy.imread(OBS_FNAME3)

function pixelError(obs,render,avg)
  diff = 0
  for i in 1:size(obs,1)
    for j in 1:size(obs,2)
      rendP = min(render[i,j],avg+90)
      #rendP = render[i,j]
      obsP = convert(Int16,obs[i,j])
      diff = diff + abs(obsP-rendP)
      #OBS_IMAGE3[i,j] = convert(Uint8,abs(obsP-rendP))
    end
  end

  return diff
end

function avgColor(obs)
  sum = 0
  for i in 1:size(obs,1)
    for j in 1:size(obs,2)
      sum = sum +  convert(Int16,obs[i,j])

    end
  end
  avg = sum / (size(obs,1)*size(obs,2))
  return avg
end


########### USER DIAGNOSTICS ##############
# plt.ion()
function debug_callback(TRACE)
	global IMAGE_COUNTER
  global CMDS
  global CMDSB
	println("LOGL=>", TRACE["ll"])
  CMDSB = CMDS
	scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/",string(IMAGE_COUNTER),".png",), TRACE["PROGRAM_OUTPUT"])
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/diff10.png",), OBS_IMAGE3)
	IMAGE_COUNTER += 1
end
#=
imgDir = readdir("C:/Users/Alan/Documents/SudokuProject/samples/st")
for i in 19:size(imgDir,1)
  println(imgDir[i])
  OBS_NAME = imgDir[i]
  load_program(PROGRAM)
  OBS_FNAME = "C:/Users/Alan/Documents/SudokuProject/samples/st/" * imgDir[i]
  OBS_IMAGE = scpy.imread(OBS_FNAME)
  OBS_EDGE = int(scpy.imread(OBS_FNAME,true))/255.0
  OBS_EDGE = edge.canny(OBS_IMAGE, sigma=1.0)
  dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_EDGE)
  OBSERVATIONS["dist_obs"] = dist_obs
  load_observations(OBSERVATIONS)
  init()
  infer(debug_callback,150,"CYCLE")
  PROGRAM2()

end
=#


println("Start")
load_program(PROGRAM)
load_observations(OBSERVATIONS)
init()
infer(debug_callback,450,"CYCLE")
println("Finish")
println("Start")
PROGRAM2()
println("Finish")



