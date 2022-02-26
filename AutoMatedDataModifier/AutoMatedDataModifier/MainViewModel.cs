using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Text;
using System.Linq;
using Newtonsoft.Json;
using System.Windows.Input;
using System.Diagnostics;
using System.Windows;
using Microsoft.Win32;
using System.Runtime.InteropServices;
using System.IO;

namespace AutoMatedDataModifier {
    public class MainViewModel : BaseViewModel {
        public MainViewModel() {
            Init();

            InsertPrevCommand = new RelayCommand(InsertPrevCommandImp);
            InsertNextCommand = new RelayCommand(InsertNextCommandImp);
            PrevCommand = new RelayCommand(PrevCommandImp);
            NextCommand = new RelayCommand(NextCommandImp);
            SaveCommand = new RelayCommand(SaveCommandImp);
            SaveAndRunCommand = new RelayCommand(SaveAndRunCommandImp);
        }


        #region 属性
        private string path;
        public string Path {
            get { return path; }
            set {
                path = value;
                RaisePropertyChanged("Path");
            }
        }

        private SessionModel session;
        public SessionModel Session {
            get { return session; }
            set {
                session = value;
                RaisePropertyChanged("Session");
            }
        }

        private StepActionModel currentStepAction;
        public StepActionModel CurrentStepAction {
            get { return currentStepAction; }
            set {
                currentStepAction = value;
                if(StepAction != null) {
                    CurrentStepNumber = StepAction.IndexOf(currentStepAction) + 1;
                    CurrentStepAction.StepNumber = CurrentStepNumber.ToString();
                }
                RaisePropertyChanged("CurrentStepAction");
            }
        }

        private int currentStepNumber;
        public int CurrentStepNumber {
            get { return currentStepNumber; }
            set {
                currentStepNumber = value;
                RaisePropertyChanged("CurrentStepNumber");
            }
        }
        #endregion

        public List<StepActionModel> StepAction {
            get { return Session?.Session?.StepAction; }
        }

        public List<string> LocationList { get; } = new List<string>() { "absolute", "visualization" };

        public List<string> ActionTypeList { get; } = new List<string>() { "left_mouse_click", "right_mouse_click", "mouse_move", "key_down" };



        #region Command
        public RelayCommand InsertPrevCommand { get; private set; }

        public RelayCommand InsertNextCommand { get; private set; }

        public RelayCommand PrevCommand { get; private set; }

        public RelayCommand NextCommand { get; private set; }

        public RelayCommand SaveCommand { get; private set; }

        public RelayCommand SaveAndRunCommand { get; private set; }

        #endregion



        public void Init() {
            Path = App.Path;
            if (!string.IsNullOrEmpty(Path) && File.Exists(Path)) {
                var jsonStr = DataHelper.XmlToJson(Path);
                Session = JsonConvert.DeserializeObject<SessionModel>(jsonStr);
                Session.Session.StepAction = Session.Session.StepAction.OrderBy(step => Convert.ToInt32(step.StepNumber)).ToList();

                CurrentStepAction = StepAction.FirstOrDefault();
            }
            else {
                Session = new SessionModel();
                Session.Session = new StepModel();
                Session.Session.StepAction = new List<StepActionModel>();

                Insert(new StepActionModel());
            }

        }

        public void Insert(StepActionModel stepAction, bool next = true) {
            if (next) {
                StepAction.Insert(CurrentStepNumber, stepAction);
            }
            else {
                StepAction.Insert(CurrentStepNumber - 1, stepAction);
            }
            CurrentStepAction = stepAction;
        }

        public void Prev() {
            if(currentStepNumber > 1) {
                CurrentStepAction = StepAction[currentStepNumber - 2];
            }
        }

        public void Next() {
            if (currentStepNumber < StepAction.Count) {
                CurrentStepAction = StepAction[currentStepNumber];
            }
        }

        public bool Save(bool askForCover = true) {
            try {
                for (int i = 0; i < StepAction.Count(); i++) {
                    StepAction[i].StepNumber = (i + 1).ToString();
                }
                var jsonStr = JsonConvert.SerializeObject(Session);
                var xml = DataHelper.JsonToXml(jsonStr);

                if (askForCover ) {
                    if (!string.IsNullOrEmpty(Path) && MessageBox.Show("是否覆盖保存?", "提示", MessageBoxButton.YesNo) == MessageBoxResult.Yes) {
                        xml.Save(Path);
                        return true;
                    }
                    else {
                        var folder = new SaveFileDialog();
                        folder.FileName = "defult.xml";
                        if (folder.ShowDialog() == true) {
                            var folderName = folder.FileName;
                            xml.Save(folderName);
                            return true;
                        }
                    }
                }
                else {
                    xml.Save(Path);
                    return true;
                }
               
                return false;
            }
            catch (Exception) {
                return false;
            }
          
        }

        public void DoPythonScript() {
            //AllocConsole();
            Process process = new Process();
            process.StartInfo.FileName = "python";
            process.StartInfo.Arguments = @"D:\Codes\demos\python\AutoMatedTesting2\Python\doAutomatedTest.py";
            //process.StartInfo.UseShellExecute = false;
            //process.StartInfo.RedirectStandardOutput = true;
            //process.StartInfo.RedirectStandardInput = true;
            //process.StartInfo.RedirectStandardError = true;
            process.Start();
            //process.BeginOutputReadLine();
            process.WaitForExit();
            //process.OutputDataReceived

        }

        #region CommandImp

        private void InsertPrevCommandImp() {
            Insert(new StepActionModel(), false);
        }

        private void InsertNextCommandImp() {
            Insert(new StepActionModel(), true);
        }

        private void SaveAndRunCommandImp() {
            if (Save(false)) {
                DoPythonScript();
            }
        }

        private void SaveCommandImp() {
            if (Save()) {
                MessageBox.Show("保存成功！");
            }
            else {
                MessageBox.Show("保存失败！");
            }
        }

        private void NextCommandImp() {
            Next();
        }

        private void PrevCommandImp() {
            Prev();
        }



        #endregion


    }

    public class BaseViewModel : INotifyPropertyChanged {
        public event PropertyChangedEventHandler PropertyChanged;

        public void RaisePropertyChanged(string propertyName) {
            if (PropertyChanged != null && !string.IsNullOrEmpty(propertyName)) {
                PropertyChanged(this, new PropertyChangedEventArgs(propertyName));
            }
        }
    }

    public class RelayCommand : ICommand {
        #region 字段

        readonly Func<Boolean> _canExecute;

        readonly Action _execute;

        #endregion

        #region 构造函数

        public RelayCommand(Action execute)
            : this(execute, null) {
        }

        public RelayCommand(Action execute, Func<Boolean> canExecute) {
            if (execute == null) {
                throw new ArgumentNullException("execute");
            }
            _execute = execute;
            _canExecute = canExecute;
        }

        #endregion

        #region ICommand的成员

        public event EventHandler CanExecuteChanged {
            add {
                if (_canExecute != null)
                    CommandManager.RequerySuggested += value;
            }
            remove {
                if (_canExecute != null)
                    CommandManager.RequerySuggested -= value;
            }
        }

        [DebuggerStepThrough]
        public Boolean CanExecute(Object parameter) {
            return _canExecute == null ? true : _canExecute();
        }

        public void Execute(Object parameter) {
            _execute();
        }

        #endregion

    }
}
