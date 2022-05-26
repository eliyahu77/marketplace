from mlrun import code_to_function, import_function, DataItem
import os


def get_class_data():
    fn = import_function("hub://gen_class_data")
    fn.run(params={
        "n_samples": 10_000,
        "m_features": 5,
        "k_classes": 2,
        "header": None,
        "weight": [0.5, 0.5],
        "sk_params": {"n_informative": 2},
        "file_ext": "csv"}, local=True, artifact_path="./artifacts/inputs")


def test_xgb_trainer_code_to_function():
    get_class_data()
    fn = code_to_function(name='test_xgb_trainer',
                          filename="xgb_trainer.py",
                          handler="train_model",
                          kind="local",
                          )
    fn.spec.command = "xgb_trainer.py"
    fn.run(params={
        "model_type": "classifier",
        "CLASS_tree_method": "hist",
        "CLASS_objective": "binary:logistic",
        "CLASS_booster": "gbtree",
        "FIT_verbose": 0,
        "label_column": "labels",
        "test_set": "./artifacts/test-set"},
        # local=True,
        inputs={"dataset": './artifacts/inputs/classifier-data.csv'})

    assert (os.path.exists(os.getcwd() + "/models/model.pkl"))


def test_local_xgb_trainer_import_function():
    # importing data preparation function locally
    get_class_data()

    fn = import_function("function.yaml")
    fn.run(params={
        "model_type": "classifier",
        "CLASS_tree_method": "hist",
        "CLASS_objective": "binary:logistic",
        "CLASS_booster": "gbtree",
        "FIT_verbose": 0,
        "label_column": "labels",
        "test_set": "./artifacts/test-set"},
        local=True, inputs={"dataset": './artifacts/inputs/classifier-data.csv'})

    assert (os.path.exists(os.getcwd() + "/models/model.pkl"))


# def test_xgb_trainer_regression_code_to_function():
#     from sklearn.datasets import load_boston
#     boston = load_boston()
#     import pandas as pd
#     data = pd.DataFrame(boston.data)
#     data.columns = boston.feature_names
#     data['PRICE'] = boston.target
#     data.to_csv("artifacts/boston.csv")
#
#     fn = code_to_function(name='test_xgb_trainer',
#                           filename="xgb_trainer.py",
#                           handler="train_model",
#                           kind="local",
#                           )
#     fn.run(params={
#         "model_type": "regressor",
#         "CLASS_objective": "reg:linear",
#         "FIT_verbose": 0,
#         "label_column": "PRICE",
#         "test_set": "./artifacts/test-set"},
#         inputs={"dataset": 'artifacts/boston.csv'},
#         local=True
#     )
#
#     assert (os.path.exists(os.getcwd() + "/models/model.pkl"))
