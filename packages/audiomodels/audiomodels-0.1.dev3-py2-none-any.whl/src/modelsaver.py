# -*- coding: utf-8 -*-
import tensorflow as tf

def freeze_session(session, keep_var_names=None, output_names=None, clear_devices=True):
    """
    Freezes the state of a session into a pruned computation graph.

    Creates a new computation graph where variable nodes are replaced by
    constants taking their current value in the session. The new graph will be
    pruned so subgraphs that are not necessary to compute the requested
    outputs are removed.    
    
    Parameters:
    
    - session: The TensorFlow session to be frozen.
    
    Default Keyword Parameters
    
    - keep_var_names: A list of variable names that should not be frozen. Defaults None.     
    - output_names: Names of the relevant graph outputs/operation/tensor to be written. Defaults None.
    - clear_devices: Remove the device directives from the graph for better portability. Defaults True.
    
    return The frozen graph definition.
    """
    
    graph = session.graph
    with graph.as_default():
      freeze_var_names = list(set(v.op.name for v in tf.global_variables()).difference(keep_var_names or []))
      output_names = output_names or []
      output_names += [v.op.name for v in tf.global_variables()]
      # Graph -> GraphDef ProtoBuf
      input_graph_def = graph.as_graph_def()
      if clear_devices:
        for node in input_graph_def.node:
          node.device = ""
      frozen_graph = convert_variables_to_constants(session, input_graph_def,
                                                    output_names, freeze_var_names)
      return frozen_graph
    
def save_model(sess, model_name='./model.pb', output_names=True):
    
  frozen_graph = freeze_session(sess, output_names= output_names)
  tf.train.write_graph(frozen_graph, "model", model_name, as_text=False)   
