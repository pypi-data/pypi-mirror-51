from sparknlp.internal import ExtendedJavaWrapper


class NorvigSpellEvaluation(ExtendedJavaWrapper):

    def __init__(self, spark, test_file, ground_truth_file):
        ExtendedJavaWrapper.__init__(self, "com.johnsnowlabs.nlp.eval.spell.NorvigSpellEvaluation", spark._jsparkSession, test_file, ground_truth_file)

    def computeAccuracyAnnotator(self, train_file, spell):
        input_cols = spell.getInputCols()
        output_col = spell.getOutputCol()
        java_input_cols = self.new_java_array_string(input_cols)
        return self._java_obj.computeAccuracyAnnotator(train_file, java_input_cols, output_col, spell.dictionary_path)

    def computeAccuracyModel(self, spell):
        return self._java_obj.computeAccuracyModel(spell._java_obj)


class SymSpellEvaluation(ExtendedJavaWrapper):

    def __init__(self, spark, test_file, ground_truth_file):
        ExtendedJavaWrapper.__init__(self, "com.johnsnowlabs.nlp.eval.spell.SymSpellEvaluation", spark._jsparkSession, test_file, ground_truth_file)

    def computeAccuracyAnnotator(self, train_file, spell):
        input_cols = spell.getInputCols()
        output_col = spell.getOutputCol()
        java_input_cols = self.new_java_array_string(input_cols)
        return self._java_obj.computeAccuracyAnnotator(train_file, java_input_cols, output_col, spell.dictionary_path)

    def computeAccuracyModel(self, spell):
        return self._java_obj.computeAccuracyModel(spell._java_obj)


class NerDLEvaluation(ExtendedJavaWrapper):

    def __init__(self, spark, test_file, tag_level=""):
        ExtendedJavaWrapper.__init__(self, "com.johnsnowlabs.nlp.eval.ner.NerDLEvaluation", spark._jsparkSession, test_file, tag_level)

    def computeAccuracyModel(self, ner):
        return self._java_obj.computeAccuracyModel(ner._java_obj)

    def computeAccuracyAnnotator(self, train_file, ner, embeddings):
        ner_params = self.__getNerParams(ner)
        embeddings_params = self.__getEmbeddingsParams(embeddings)
        return self._java_obj.computeAccuracyAnnotator(train_file, ner_params['input_cols'], ner_params['output_col'],
                                                       ner_params['random_seed'], ner_params['label_column'],
                                                       embeddings_params['input_cols'], embeddings_params['output_col'],
                                                       embeddings_params['path'], embeddings_params['dimension'],
                                                       embeddings_params['format'])

    def __getNerParams(self, ner):
        ner_params = dict()
        input_cols = ner.getInputCols()
        ner_params['input_cols'] = self.new_java_array_string(input_cols)
        ner_params['output_col'] = ner.getOutputCol()
        ner_params['label_column'] = ner.getLabelColumn()
        ner_params['random_seed'] = ner.getRandomSeed()
        return ner_params

    def __getEmbeddingsParams(self, embeddings):
        embeddings_params = dict()
        input_cols = embeddings.getInputCols()
        embeddings_params['input_cols'] = self.new_java_array_string(input_cols)
        embeddings_params['output_col'] = embeddings.getOutputCol()
        embeddings_params['path'] = embeddings.getEmbeddingsPath()
        embeddings_params['dimension'] = embeddings.getDimension()
        embeddings_params['format'] = embeddings.getFormat()
        return embeddings_params


class NerCrfEvaluation(ExtendedJavaWrapper):

    def __init__(self, spark, test_file, tag_level=""):
        ExtendedJavaWrapper.__init__(self, "com.johnsnowlabs.nlp.eval.ner.NerCrfEvaluation", spark._jsparkSession, test_file, tag_level)

    def computeAccuracyModel(self, ner):
        return self._java_obj.computeAccuracyModel(ner._java_obj)

    def computeAccuracyAnnotator(self, train_file, ner, embeddings):
        ner_params = self.__getNerParams(ner)
        embeddings_params = self.__getEmbeddingsParams(embeddings)
        return self._java_obj.computeAccuracyAnnotator(train_file, ner_params['input_cols'], ner_params['output_col'],
                                                       ner_params['random_seed'], ner_params['label_column'],
                                                       embeddings_params['input_cols'], embeddings_params['output_col'],
                                                       embeddings_params['path'], embeddings_params['dimension'],
                                                       embeddings_params['format'])

    def __getNerParams(self, ner):
        ner_params = dict()
        input_cols = ner.getInputCols()
        ner_params['input_cols'] = self.new_java_array_string(input_cols)
        ner_params['output_col'] = ner.getOutputCol()
        ner_params['label_column'] = ner.getLabelColumn()
        ner_params['random_seed'] = ner.getRandomSeed()
        return ner_params

    def __getEmbeddingsParams(self, embeddings):
        embeddings_params = dict()
        input_cols = embeddings.getInputCols()
        embeddings_params['input_cols'] = self.new_java_array_string(input_cols)
        embeddings_params['output_col'] = embeddings.getOutputCol()
        embeddings_params['path'] = embeddings.getEmbeddingsPath()
        embeddings_params['dimension'] = embeddings.getDimension()
        embeddings_params['format'] = embeddings.getFormat()
        return embeddings_params


class POSEvaluation(ExtendedJavaWrapper):

    def __init__(self, spark, test_file):
        ExtendedJavaWrapper.__init__(self, "com.johnsnowlabs.nlp.eval.POSEvaluation", spark._jsparkSession, test_file)

    def computeAccuracyModel(self, pos):
        return self._java_obj.computeAccuracyModel(pos._java_obj)

    def computeAccuracyAnnotator(self, train_file, pos):
        pos_params = self.__getPosParams(pos)
        return self._java_obj.computeAccuracyAnnotator(train_file, pos_params['input_cols'], pos_params['output_col'],
                                                       pos_params['number_iterations'])

    def __getPosParams(self, pos):
        pos_params = dict()
        input_cols = pos.getInputCols()
        pos_params['input_cols'] = self.new_java_array_string(input_cols)
        pos_params['output_col'] = pos.getOutputCol()
        pos_params['number_iterations'] = pos.getNIterations()
        return pos_params
