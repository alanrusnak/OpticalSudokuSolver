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
OBS_IMAGE = scpy.imread(OBS_FNAME)
OBS_EDGE = int(scpy.imread(OBS_FNAME,true))/255.0
OBS_EDGE = edge.canny(OBS_IMAGE, sigma=1.0)
#OBS_IMAGE = pyeval("canny(OBS_IMAGE,1.0)", canny = edge.canny, OBS_IMAGE=OBS_IMAGE)
#scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/obs_image3.png",), OBS_IMAGE)
#calculate and store distance transform
dist_obs = pyeval("dt(npinvert(im))", npinvert=np.invert, dt=scp_morph.distance_transform_edt, im=OBS_EDGE)
OBSERVATIONS["dist_obs"] = dist_obs

global CMDSB = ""
global CMDS = ""
#CMDSB = "4.0375301777753_3.9199065172991676_17.808414694543075_4.4517305152536_5.221429647909042_0"

iterations = 0
minD = typemax(Int64)
function PROGRAM()
  global CMDS
  global CMDSB
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)



	CMDS = Dict()
	cnt=1;

  #=
  ex = Uniform(3.9,4.2,1,1)
  ey = Uniform(3.7,4.1,1,1)
  ez = Uniform(16,18,1,1)
  cx = Uniform(4.3,4.7,1,1)
  cy = Uniform(4.3,4.7,1,1)
  r = Uniform(0.3,1,1,1)
  cz = 0
  =#

  ex = Uniform(3.5,4,1,1)
  ey = Uniform(5,6,1,1)
  ez = Uniform(15,17,1,1)
  cx = Uniform(4,5,1,1)
  cy = Uniform(4.5,6,1,1)
  r = Uniform(-0.5,0,1,1)
  cz = 0


  CMDS = string(ex) * "_" * string(ey) * "_" * string(ez) * "_" * string(cx) * "_" * string(cy) * "_" * string(r)
  #CMDSB = CMDS


	rendering = render(CMDS)
  #edgemap = rendering


  if(iterations<500)
	  edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering)
  #edgemap = edge.canny(rendering, sigma=1.0)
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/c",string(IMAGE_COUNTER),".png",), edgemap)



	#calculate distance transform
	# dist_obs = scp_morph.distance_transform_edt(~OBSERVATIONS["IMAGE"])
	  valid_indxs = pyeval("npwhere(edgemap>0)", npwhere=np.where,edgemap=edgemap)
	#valid_indxs = np.where(edgemap > 0)

	  D = pyeval("npmultiply(dist_obs[valid_indxs], ren[valid_indxs])",npmultiply=np.multiply, dist_obs=OBSERVATIONS["dist_obs"],valid_indxs=valid_indxs, ren=edgemap)


  else
    D = pixelError2(OBS_IMAGE,rendering)
    #=
    if(iterations==100)
      minD = D
      CMDSB = CMDS
    end
    if(D<minD)
      minD = D
      CMDSB = CMDS
    end
    =#

  end


  observe(0,Normal(0,0.35),D)

	return rendering
end

function PROGRAM2()
  global CMDS
  global CMDSB
	LINE=Stack(Int);FUNC=Stack(Int);LOOP=Stack(Int)



	CMDS = Dict()
	cnt=1;


  CMDS = CMDSB * "_"

  minChar = 0
  minDiff = typemax(Int64)

  for i in 1:81
    for j in 0:9
      if(j==0)
        CMDSTry = CMDS * string(j)
        rendering = render(CMDSTry)
        minDiff = pixelError(OBS_IMAGE,rendering)
        minChar = j
      else
        CMDSTry = CMDS * string(j)
        rendering = render(CMDSTry)
        pError = pixelError(OBS_IMAGE,rendering)
        if(pError<minDiff)
          minDiff = pError
          minChar = j
        end
      end
    end
    println(i)
    CMDS = CMDS * string(minChar)
    minDiff = typemax(Int64)
  end

  rendering = render(CMDS)
  scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/final8.png",), rendering)
  println(CMDS)


  #edgemap = rendering

	#edgemap = pyeval("canny(rendering,1.0)", canny = edge.canny, rendering=rendering)
  #edgemap = edge.canny(rendering, sigma=1.0)
  #scpy.imsave(string("C:/Users/Alan/Documents/SudokuProject/output/c",string(IMAGE_COUNTER),".png",), edgemap)



	#calculate distance transform
	# dist_obs = scp_morph.distance_transform_edt(~OBSERVATIONS["IMAGE"])
	#valid_indxs = pyeval("npwhere(edgemap>0)", npwhere=np.where,edgemap=edgemap)
	#valid_indxs = np.where(edgemap > 0)

  #x = time()
  #D = pixelError(OBS_IMAGE,rendering)
  #print((time()-x)*1000)

	#constraint to observation
  #sigma = Uniform(0.1,1,1,1)
  #observe(0,Normal(0,0.35),D)


	return rendering
end

  OBS_FNAME3 = "C:/Users/Alan/Documents/SudokuProject/diff10.png"
  OBS_IMAGE3 = scpy.imread(OBS_FNAME3)

function pixelError(obs,render)
  diff = 0
  for i in 1:size(obs,1)
    for j in 1:size(obs,2)
      rendP = min(render[i,j],180)
      #rendP = render[i,j]
      obsP = convert(Int16,obs[i,j])
      diff = diff + abs(obsP-rendP)
      #OBS_IMAGE3[i,j] = convert(Uint8,abs(obsP-rendP))
    end
  end

  return diff
end

function pixelError2(obs,render)
  diff = 0
  for i in 1:size(obs,1)
    for j in 1:size(obs,2)
      rendP = convert(Int16,render[i,j])
      obsP = convert(Int16,obs[i,j])
      diff = diff + abs(obsP-rendP)
      #OBS_IMAGE3[i,j] = convert(Uint8,abs(obsP-rendP))
    end
  end

  return diff
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

println("Start")
load_program(PROGRAM)
load_observations(OBSERVATIONS)
init()
infer(debug_callback,250,"CYCLE")
println("Finish")
println("Start")
PROGRAM2()
#load_program(PROGRAM2)
#load_observations(OBSERVATIONS)
#init()
#infer(debug_callback,5000,"CYCLE")
#infer(debug_callback, 1,"s00", "Gibbs", "","")
println("Finish")
# plt.show(block=true)


