"""Dataloader for language generation"""
from collections import Counter
from itertools import chain

import numpy as np

from nltk.tokenize import WordPunctTokenizer
# from .._utils.unordered_hash import UnorderedSha256
from .._utils.file_utils import get_resource_file_path
from .._utils import hooks
from .dataloader import LanguageProcessingBase
from ..metric import MetricChain, PerplexityMetric, LanguageGenerationRecorder, \
	FwBwBleuCorpusMetric, SelfBleuCorpusMetric

# pylint: disable=W0223
class LanguageGeneration(LanguageProcessingBase):
	r"""Base class for language modelling datasets. This is an abstract class.

	This class is supported for language modeling tasks or language generation tasks
	without any inputs.

	Arguments:{ARGUMENTS}

	Attributes:{ATTRIBUTES}
	"""

	ARGUMENTS = LanguageProcessingBase.ARGUMENTS
	ATTRIBUTES = LanguageProcessingBase.ATTRIBUTES

	def get_batch(self, key, indexes):
		'''{LanguageProcessingBase.GET_BATCH_DOC_WITHOUT_RETURNS}

		Returns:
			(dict): A dict at least contains:

			* **sent_length** (:class:`numpy.ndarray`): A 1-d array, the length of sentence in each batch.
			  Size: ``[batch_size]``
			* **sent** (:class:`numpy.ndarray`): A 2-d padding array containing id of words.
			  Only provide valid words. ``unk_id`` will be used if a word is not valid.
			  Size: ``[batch_size, max(sent_length)]``
			* **sent_allvocabs** (:class:`numpy.ndarray`): A 2-d padding array containing id of words.
			  Provide both valid and invalid words.
			  Size: ``[batch_size, max(sent_length)]``

		Examples:

			>>> # all_vocab_list = ["<pad>", "<unk>", "<go>", "<eos>", "how", "are", "you",
			>>> #	"hello", "i", "am", "fine"]
			>>> # vocab_size = 9
			>>> # vocab_list = ["<pad>", "<unk>", "<go>", "<eos>", "how", "are", "you", "hello", "i"]
			>>> dataloader.get_batch('train', [0, 1, 2])
			{
				"sent": numpy.array([
					[2, 4, 5, 6, 3, 0],   # first sentence: <go> how are you <eos> <pad>
					[2, 7, 3, 0, 0, 0],   # second sentence:  <go> hello <eos> <pad> <pad> <pad>
					[2, 7, 8, 1, 1, 3]    # third sentence: <go> hello i <unk> <unk> <eos>
				]),
				"sent_length": numpy.array([5, 3, 6]), # length of sentences
				"sent_allvocabs": numpy.array([
					[2, 4, 5, 6, 3, 0],   # first sentence: <go> how are you <eos> <pad>
					[2, 7, 3, 0, 0, 0],   # second sentence:  <go> hello <eos> <pad> <pad> <pad>
					[2, 7, 8, 9, 10, 3]   # third sentence: <go> hello i am fine <eos>
				]),
			}
		'''
		if key not in self.key_name:
			raise ValueError("No set named %s." % key)
		res = {}
		batch_size = len(indexes)
		res["sent_length"] = np.array( \
			list(map(lambda i: len(self.data[key]['sent'][i]), indexes)))
		res_sent = res["sent"] = np.zeros( \
			(batch_size, np.max(res["sent_length"])), dtype=int)
		for i, j in enumerate(indexes):
			sentence = self.data[key]['sent'][j]
			res["sent"][i, :len(sentence)] = sentence

		res["sent_allvocabs"] = res_sent.copy()
		res_sent[res_sent >= self.valid_vocab_len] = self.unk_id
		return res

	def get_teacher_forcing_metric(self, gen_log_prob_key="gen_log_prob"):
		'''Get metrics for teacher-forcing. In other words, this function
		provides metrics for language modelling task.

		It contains:

		* :class:`.metric.PerplexityMetric`

		Arguments:
			gen_log_prob_key (str): The key of predicted log probability over words.
				Refer to :class:`.metric.PerplexityMetric`. Default: ``gen_log_prob``.

		Returns:
			A :class:`.metric.MetricChain` object.
		'''
		metric = MetricChain()
		metric.add_metric(PerplexityMetric(self, \
					reference_allvocabs_key='sent_allvocabs', \
					reference_len_key='sent_length', \
					gen_log_prob_key=gen_log_prob_key))
		return metric

	def get_inference_metric(self, gen_key="gen", sample=1000, seed=1229, cpu_count=None):
		'''Get metrics for inference. In other words, this function provides metrics for
		language generation tasks.

		It contains:

		* :class:`.metric.SelfBleuCorpusMetric`
		* :class:`.metric.FwBwBleuCorpusMetric`
		* :class:`.metric.LanguageGenerationRecorder`

		Arguments:
			gen_key (str): The key of generated sentences in index form.
				Refer to :class:`.metric.LanguageGenerationRecorder`.
				Default: ``gen``.
			sample (int): Sample numbers for self-bleu metric.
				It will be fast but inaccurate if this become small.
				Refer to :class:`.metric.SelfBleuCorpusMetric`. Default: ``1000``.
			seed (int): Random seed for sampling.
				Refer to :class:`.metric.SelfBleuCorpusMetric`. Default: ``1229``.
			cpu_count (int): Number of used cpu for multiprocessing.
				Refer to :class:`.metric.SelfBleuCorpusMetric`. Default: ``None``.
		Returns:
			A :class:`.metric.MetricChain` object.
		'''
		metric = MetricChain()
		metric.add_metric(SelfBleuCorpusMetric(self, \
					gen_key=gen_key, \
					sample=sample, \
					seed=seed, \
					cpu_count=cpu_count))
		metric.add_metric(FwBwBleuCorpusMetric(self, \
					reference_test_list=self.get_all_batch("test")["sent"], \
					gen_key=gen_key, \
					sample=sample, \
					seed=seed, \
					cpu_count=cpu_count))
		metric.add_metric(LanguageGenerationRecorder(self, gen_key=gen_key))
		return metric

class MSCOCO(LanguageGeneration):
	'''A dataloader for preprocessed MSCOCO dataset.

	Arguments:
		file_id (str): A string indicating the source of MSCOCO dataset. Default: ``resources://MSCOCO``.
				A preset dataset is downloaded and cached.
		valid_vocab_times (int): A cut-off threshold of valid tokens. All tokens appear
				not less than `min_vocab_times` in **training set** will be marked as valid words.
				Default: ``10``.
		max_sent_length (int): All sentences longer than ``max_sent_length`` will be shortened
				to first ``max_sent_length`` tokens. Default: ``50``.
		invalid_vocab_times (int):  A cut-off threshold of invalid tokens. All tokens appear
				not less than ``invalid_vocab_times`` in the **whole dataset** (except valid words) will be
				marked as invalid words. Otherwise, they are unknown words, which are ignored both for
				model or metrics. Default: ``0`` (No unknown words).

	Refer to :class:`.LanguageGeneration` for attributes and methods.

	References:
		[1] http://images.cocodataset.org/annotations/annotations_trainval2017.zip

		[2] Chen X, Fang H, Lin T Y, et al. Microsoft COCO Captions:
		Data Collection and Evaluation Server. arXiv:1504.00325, 2015.

	'''

	@hooks.hook_dataloader
	def __init__(self, file_id="resources://MSCOCO", min_vocab_times=10, \
			max_sent_length=50, invalid_vocab_times=0):
		self._file_id = file_id
		self._file_path = get_resource_file_path(file_id)
		self._min_vocab_times = min_vocab_times
		self._max_sent_length = max_sent_length
		self._invalid_vocab_times = invalid_vocab_times
		super().__init__()

	def _load_data(self):
		r'''Loading dataset, invoked during the initialization of :class:`LanguageGeneration`.
		'''
		origin_data = {}
		for key in self.key_name:
			f_file = open("%s/mscoco_%s.txt" % (self._file_path, key), 'r', encoding='utf-8')
			origin_data[key] = {}
			origin_data[key]['sent'] = list( \
				map(lambda line: line.split(), f_file.readlines()))

		raw_vocab_list = list(chain(*(origin_data['train']['sent'])))
		# Important: Sort the words preventing the index changes between
		# different runs
		vocab = sorted(Counter(raw_vocab_list).most_common(), \
					   key=lambda pair: (-pair[1], pair[0]))
		left_vocab = list( \
			filter( \
				lambda x: x[1] >= self._min_vocab_times, \
				vocab))
		vocab_list = self.ext_vocab + list(map(lambda x: x[0], left_vocab))
		valid_vocab_len = len(vocab_list)
		valid_vocab_set = set(vocab_list)

		for key in self.key_name:
			if key == 'train':
				continue
			raw_vocab_list.extend(list(chain(*(origin_data[key]['sent']))))
		vocab = sorted(Counter(raw_vocab_list).most_common(), \
					   key=lambda pair: (-pair[1], pair[0]))
		left_vocab = list( \
			filter( \
				lambda x: x[1] >= self._invalid_vocab_times and x[0] not in valid_vocab_set, \
				vocab))
		vocab_list.extend(list(map(lambda x: x[0], left_vocab)))

		print("valid vocab list length = %d" % valid_vocab_len)
		print("vocab list length = %d" % len(vocab_list))

		word2id = {w: i for i, w in enumerate(vocab_list)}
		def line2id(line):
			return ([self.go_id] + \
					list(map(lambda word: word2id[word] if word in word2id else self.unk_id, line)) \
					+ [self.eos_id])[:self._max_sent_length]

		data = {}
		data_size = {}
		for key in self.key_name:
			data[key] = {}
			data[key]['sent'] = list(map(line2id, origin_data[key]['sent']))
			data_size[key] = len(data[key]['sent'])

			vocab = list(chain(*(origin_data[key]['sent'])))
			vocab_num = len(vocab)
			oov_num = len( \
				list( \
					filter( \
						lambda word: word not in word2id, \
						vocab)))
			invalid_num = len( \
				list( \
					filter( \
						lambda word: word not in valid_vocab_set, \
						vocab))) - oov_num
			length = list( \
				map(len, origin_data[key]['sent']))
			cut_num = np.sum( \
				np.maximum( \
					np.array(length) - \
					self._max_sent_length + \
					1, \
					0))
			print( \
				"%s set. invalid rate: %f, unknown rate: %f, max length before cut: %d, cut word rate: %f" % \
				(key, invalid_num / vocab_num, oov_num / vocab_num, max(length), cut_num / vocab_num))
		return vocab_list, valid_vocab_len, data, data_size

	def tokenize(self, sentence):
		r'''Convert sentence(str) to list of token(str)

		Arguments:
			sentence (str)

		Returns:
			sent (list): list of token(str)
		'''
		return WordPunctTokenizer().tokenize(sentence)
