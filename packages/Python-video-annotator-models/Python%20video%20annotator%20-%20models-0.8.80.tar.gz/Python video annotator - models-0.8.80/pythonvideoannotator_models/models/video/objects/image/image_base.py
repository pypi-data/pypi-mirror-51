from pythonvideoannotator_models.models.video.objects.video_object import VideoObject


class ImageBase(VideoObject):

	def __init__(self, video):
		super(ImageBase, self).__init__()

		self.name 	= video.generate_child_name('Image ')
		self.image 	= None

		self._video = video
		self._video += self

	######################################################################
	### OBJECT FUNCTIONS #################################################
	######################################################################
		
	######################################################################
	### CLASS FUNCTIONS ##################################################
	######################################################################

	def __str__(self): return self.name
	
	######################################################################
	### PROPERTIES #######################################################
	######################################################################
