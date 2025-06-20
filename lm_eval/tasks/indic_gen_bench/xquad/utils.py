import transformers.data.metrics.squad_metrics as squad_metrics

def process_results_qa(doc, results):
    preds = results[0]
    reference = doc_to_target(doc)
    f1_sum = squad_metrics.compute_f1(reference, preds)
    exact_match = squad_metrics.compute_exact(reference, preds)
    return {"f1": f1_sum, "exact_match": exact_match}