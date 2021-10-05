package hex.anovaglm;

import hex.*;
import hex.deeplearning.DeepLearningModel;
import hex.glm.GLM;
import hex.glm.GLMModel;
import org.apache.commons.math3.distribution.FDistribution;
import water.*;
import water.fvec.Frame;
import water.fvec.Vec;
import water.udf.CFuncRef;
import water.util.TwoDimTable;

import java.io.Serializable;
import java.util.Arrays;

import static hex.anovaglm.ANOVAGLMUtils.generateGLMSS;
import static hex.glm.GLMModel.GLMParameters.*;
import static hex.glm.GLMModel.GLMParameters.Family.AUTO;


public class ANOVAGLMModel extends Model<ANOVAGLMModel, ANOVAGLMModel.ANOVAGLMParameters, ANOVAGLMModel.ANOVAGLMModelOutput>{
  public ANOVAGLMModel(Key<ANOVAGLMModel> selfKey, ANOVAGLMParameters parms, ANOVAGLMModelOutput output) {
    super(selfKey, parms, output);
  }

  @Override
  public ModelMetrics.MetricBuilder makeMetricBuilder(String[] domain) {
    assert domain == null;
    switch (_output.getModelCategory()) {
      case Binomial:
        return new ModelMetricsBinomial.MetricBuilderBinomial(domain);
      case Multinomial:
        return new ModelMetricsMultinomial.MetricBuilderMultinomial(_output.nclasses(), domain, _parms._auc_type);
      case Regression:
        return new ModelMetricsRegression.MetricBuilderRegression();
      default:
        throw H2O.unimpl("Invalid ModelCategory " + _output.getModelCategory());
    }
  }

  @Override
  protected double[] score0(double[] data, double[] preds) {
    throw new UnsupportedOperationException("ANOVAGLM does not support scoring on data.  It only provide information" +
            " on predictor relevance");
  }

  @Override
  public Frame score(Frame fr, String destination_key, Job j, boolean computeMetrics, CFuncRef customMetricFunc) {
    throw new UnsupportedOperationException("ANOVAGLM does not support scoring on data.  It only provide information" +
            " on predictor relevance");
  }

  /***
   * Return the ANOVA table as an H2OFrame per seb suggestion
   * @return H2O Frame containing the ANOVA table as in the model summary
   */
  public Frame result() {
    assert _output._result_frame_key!= null : "ANOVA Table Key is null";
    return DKV.getGet(_output._result_frame_key);
  }
  
  public static class ANOVAGLMParameters extends Model.Parameters {
    public int _highest_interaction_term;
    public double[] _alpha;
    public double[] _lambda = new double[]{0};
    public boolean _standardize = true;
    public Family _family = AUTO;
    public boolean lambda_search;
    public Link _link = Link.family_default;
    public Solver _solver = Solver.IRLSM;
    public String[] _interactions=null;
    public double _tweedie_variance_power;
    public double _tweedie_link_power=1.0;
    public double _theta;
    public double _invTheta;
    public Serializable _missing_values_handling = MissingValuesHandling.MeanImputation;
    public boolean _compute_p_values = true;
    public boolean _remove_collinear_columns = true;
    public int _nfolds = 0; // disable cross-validation
    public Key<Frame> _plug_values = null;
    public boolean _save_transformed_framekeys = false; // for debugging, save the transformed predictors/interaction
    public int _nparallelism = 4;

    @Override
    public String algoName() {
      return "ANOVAGLM";
    }

    @Override
    public String fullName() {
      return "ANOVA for Generalized Linear Model";
    }

    @Override
    public String javaName() { return ANOVAGLMModel.class.getName(); }

    @Override
    public long progressUnits() {
      return 1;
    }

    public MissingValuesHandling missingValuesHandling() {
      if (_missing_values_handling instanceof MissingValuesHandling)
        return (MissingValuesHandling) _missing_values_handling;
      assert _missing_values_handling instanceof DeepLearningModel.DeepLearningParameters.MissingValuesHandling;
      switch ((DeepLearningModel.DeepLearningParameters.MissingValuesHandling) _missing_values_handling) {
        case MeanImputation:
          return MissingValuesHandling.MeanImputation;
        case Skip:
          return MissingValuesHandling.Skip;
        default:
          throw new IllegalStateException("Unsupported missing values handling value: " + _missing_values_handling);
      }
    }

    public boolean imputeMissing() {
      return missingValuesHandling() == MissingValuesHandling.MeanImputation ||
              missingValuesHandling() == MissingValuesHandling.PlugValues;
    }

    public DataInfo.Imputer makeImputer() {
      if (missingValuesHandling() == MissingValuesHandling.PlugValues) {
        if (_plug_values == null || _plug_values.get() == null) {
          throw new IllegalStateException("Plug values frame needs to be specified when Missing Value Handling = PlugValues.");
        }
        return new GLM.PlugValuesImputer(_plug_values.get());
      } else { // mean/mode imputation and skip (even skip needs an imputer right now! PUBDEV-6809)
        return new DataInfo.MeanImputer();
      }
    }
  }

  public static class ANOVAGLMModelOutput extends Model.Output {
    DataInfo _dinfo;
    public long _training_time_ms;
    public String[][] _coefficient_names; // coefficient names of all models
    Family _family;
    public Key<Frame> _transformed_columns_key;
    public Key<Frame> _result_frame_key;
    public TwoDimTable[] _coefficients_table;

    @Override
    public ModelCategory getModelCategory() {
      switch (_family) {
        case quasibinomial:
        case fractionalbinomial:
        case binomial: return ModelCategory.Binomial;
        case multinomial: return ModelCategory.Multinomial;
        case ordinal: return ModelCategory.Ordinal;
        default: return ModelCategory.Regression;
      }
    }

    public String[][] coefficientNames() { return _coefficient_names; }

    public ANOVAGLMModelOutput(ANOVAGLM b, DataInfo dinfo) {
      super(b, dinfo._adaptedFrame);
      _dinfo = dinfo;
      _domains = dinfo._adaptedFrame.domains();
      _family = b._parms._family;
    }
  }
  
  public void fillOutput(String[] modelNames, GLMModel[] glmModels, int[] degreeOfFreedom) {
    _output._result_frame_key = generateANOVATableFrame(modelNames, glmModels, degreeOfFreedom);
    _output._model_summary = generateSummary();
  }

  /**
   * The Type III SS calculation, degree of freedom, F-statistics and p-values will be included in the model
   * summary.  For details on how those are calculated, refer to ANOVAGLMTutorial  
   * https://h2oai.atlassian.net/browse/PUBDEV-8088 section V.
   * 
   * @return a {@link TwoDimTable} representation of the result frame
   */
  public TwoDimTable generateSummary(){
    assert _output._result_frame_key != null;
    Frame result = _output._result_frame_key.get();
    assert result != null;
    int ncols = result.numCols();
    int nrows = (int) result.numRows();
    String[] names = result.names();
    String[] types = new String[]{"string", "string", "string", "double", "int", "double", "double", "double"};
    String[] formats = new String[]{"%s", "%s", "%s", "%f", "%d", "%f", "%f", "%f"};
    String[] rowHeaders = new String[nrows];
    TwoDimTable table = new TwoDimTable("GLM ANOVA Type III SS", "summary", 
            rowHeaders, names, types, formats, "");
    
    for (int rIdx = 0; rIdx < nrows; rIdx++) {
      for (int cIdx = 0; cIdx < ncols; cIdx++) {
        Vec v = result.vec(cIdx);
        table.set(rIdx, cIdx, v.isNumeric() ? v.at(rIdx) : v.stringAt(rIdx));
        if (cIdx == 0) rowHeaders[rIdx] = v.stringAt(rIdx);
      }
    }
    return table;
  }

  public Key<Frame> generateANOVATableFrame(String[] modelNames, GLMModel[] glmModels, int[] degreeOfFreedom) {
    int lastModelIndex = glmModels.length - 1;
    String[] colNames = new String[]{"predictors_interactions", "family", "link", "ss", "df", "ms", "f", "p_value"};
    String[] rowNames = new String[lastModelIndex];
    String[] familyNames = new String[lastModelIndex];
    String[] linkNames = new String[lastModelIndex];
    double[] ss = generateGLMSS(glmModels, _parms._family);
    double[] dof = Arrays.stream(degreeOfFreedom).asDoubleStream().toArray();
    double[] msA = new double[lastModelIndex];
    double[] fA = new double[lastModelIndex];
    double[] pValues = new double[lastModelIndex];

    System.arraycopy(modelNames, 0, rowNames, 0, lastModelIndex);
    long dofFullModel = glmModels[lastModelIndex]._output._training_metrics.residual_degrees_of_freedom();
    double mse = ss[lastModelIndex]/dofFullModel;
    double oneOverMse = 1.0/mse;
    for (int rIndex = 0; rIndex < lastModelIndex; rIndex++) {
      familyNames[rIndex] = _parms._family.toString();
      linkNames[rIndex] = _parms._link.toString();
      
      double ms = ss[rIndex]/degreeOfFreedom[rIndex];
      msA[rIndex] = ms;
      
      double f = oneOverMse*ss[rIndex]/degreeOfFreedom[rIndex];
      fA[rIndex] = f;

      FDistribution fdist = new FDistribution(degreeOfFreedom[rIndex], dofFullModel);
      double p_value = 1.0 - fdist.cumulativeProbability(f);
      pValues[rIndex] = p_value;
    }
    
    Vec.VectorGroup vg = Vec.VectorGroup.VG_LEN1;
    Vec rNames = Vec.makeVec(rowNames, vg.addVec());
    Vec fNames = Vec.makeVec(familyNames, vg.addVec());
    Vec lNames = Vec.makeVec(linkNames, vg.addVec());
    Vec sumSquares = Vec.makeVec(ss, vg.addVec());
    Vec degOfFreedom = Vec.makeVec(dof, vg.addVec());
    Vec msV = Vec.makeVec(msA, vg.addVec());
    Vec fV = Vec.makeVec(fA, vg.addVec());
    Vec pValuesV = Vec.makeVec(pValues, vg.addVec());
    Frame anovaFrame = new Frame(Key.<Frame>make(), colNames, new Vec[]{rNames, fNames, lNames, sumSquares, 
            degOfFreedom, msV, fV, pValuesV});
    DKV.put(anovaFrame);
    return anovaFrame._key;
  }
  
  @Override
  protected Futures remove_impl(Futures fs, boolean cascade) {
    super.remove_impl(fs, cascade);
    Keyed.remove(_output._result_frame_key, fs, true);
    Keyed.remove(_output._transformed_columns_key, fs, true);
    return fs;
  }

  @Override
  protected AutoBuffer writeAll_impl(AutoBuffer ab) {
    if (_output._result_frame_key != null) ab.putKey(_output._result_frame_key);
    if (_output._transformed_columns_key != null) ab.putKey(_output._transformed_columns_key);
    return super.writeAll_impl(ab);
  }
}
