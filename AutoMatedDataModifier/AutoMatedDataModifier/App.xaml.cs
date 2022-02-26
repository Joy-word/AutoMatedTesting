using System;
using System.Collections.Generic;
using System.Configuration;
using System.Data;
using System.Linq;
using System.Threading.Tasks;
using System.Windows;

namespace AutoMatedDataModifier {
    /// <summary>
    /// Interaction logic for App.xaml
    /// </summary>
    public partial class App : Application {
        protected override void OnStartup(StartupEventArgs e) {
            base.OnStartup(e);
            if(e.Args != null && e.Args.Count() > 0) {
                Path = e.Args[0];
            }
        }

        public static string Path { get; set; }
    }
}
