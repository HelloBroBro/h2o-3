package hex.genmodel.algos.tree;

import hex.genmodel.tools.PrintMojo;

import java.io.PrintStream;
import java.util.*;

/**
 * Graph for representing a GBM or DRF forest.
 * A graph contains subgraphs (trees).
 */
public class SharedTreeGraph {

  public final ArrayList<SharedTreeSubgraph> subgraphArray = new ArrayList<>();

  /**
   * Make a new forest.
   */
  public SharedTreeGraph() {
  }

  /**
   * Make a new tree.
   * @param name Tree name.
   * @return The new tree.
   */
  public SharedTreeSubgraph makeSubgraph(String name) {
    SharedTreeSubgraph sg = new SharedTreeSubgraph(subgraphArray.size(), name);
    subgraphArray.add(sg);
    return sg;
  }

  /**
   * Debug printout of graph structure.
   * For developer use only.
   */
  public void print() {
    System.out.println("------------------------------------------------------------");
    System.out.println("Graph");
    for (SharedTreeSubgraph sg : subgraphArray) {
      sg.print();
    }
  }

  public SharedTreeNode walkNodes(int subgraphId, String path) {
    return subgraphArray.get(subgraphId).walkNodes(path);
  }

  /**
   * Print graph output in a format readable by dot (graphviz).
   * @param os Stream to write the output to
   * @param maxLevelsToPrintPerEdge Limit the number of individual categorical level names printed per edge
   * @param detail include addtional node detail information
   * @param optionalTitle Optional title to override the default
   * @param treeOptions object of PrintTreeOptions to control how trees are printed in terms of font size and number of decimal places for numerical values
   *
   */
  public void printDot(PrintStream os, int maxLevelsToPrintPerEdge, boolean detail, String optionalTitle, PrintMojo.PrintTreeOptions treeOptions) {
    os.println("/*");
    os.println("Generated by:");
    os.println("    http://https://github.com/h2oai/h2o-3/tree/master/h2o-genmodel/src/main/java/hex/genmodel/tools/PrintMojo.java");
    os.println("*/");
    os.println("");
    os.println("/*");
    os.println("On a mac:");
    os.println("");
    os.println("$ brew install graphviz");
    os.println("$ dot -Tpng file.gv -o file.png");
    os.println("$ open file.png");
    os.println("*/");
    os.println("");
    os.println("digraph G {");
    for (SharedTreeSubgraph sg : subgraphArray) {
      sg.printDot(os, maxLevelsToPrintPerEdge, detail, optionalTitle, treeOptions);
    }
    os.println("");
    os.println("}");
    os.println("");
  }
  
  public List<Map<String, Object>> toJson() {
    List<Map<String, Object>> trees = new ArrayList<>();
    for (SharedTreeSubgraph sg : subgraphArray) {
      trees.add(sg.toJson());
    }
    return trees;
  }

  @Override
  public boolean equals(Object o) {
    if (this == o) return true;
    if (o == null || getClass() != o.getClass()) return false;
    SharedTreeGraph that = (SharedTreeGraph) o;
    return Objects.equals(subgraphArray, that.subgraphArray);
  }

  @Override
  public int hashCode() {
    return Objects.hash(subgraphArray);
  }

}
