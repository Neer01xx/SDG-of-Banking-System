import numpy
import uuid
import json

class SimUtils():

  @classmethod
  def gen_uuid_id(cls):
    return str(uuid.uuid4())[-12:]

  @classmethod
  def get_json(cls, url):
    f = open(url)
    data = json.load(f)
    return data

  @classmethod
  def randomize(cls, params):
    
    #1- Normal
    if params["type"] == "normal":
      x = numpy.random.normal(params["loc"], params["scale"])
      if x < 0:
        return params["loc"]
      return x

    #2- LogNormal
    if params["type"] == "lognormal":
      x = numpy.random.lognormal(params["mean"], params["std"])
      if x < 0:
        return params["mean"]
      return x

    #3- Exponential
    if params["type"] == "exponential":
      x = numpy.random.exponential(params["scale"])
      if x < 0:
        return params["scale"]
      return x
    
    #4- Inverse Exonentential 
    if params["type"] == "inverse_exponential":
      x = 1 - numpy.random.exponential(params["scale"])
      if x < 0:
        return 1 - params["scale"]
      return x
      
    #5- Uniform
    if params["type"] == "uniform":
      x = numpy.random.uniform(params["low"], params["high"])
      if x < 0:
        return params["low"]
      return x
    
    # Constant Value Returned
    if params["type"] == "constant":
      return params["value"]
 
