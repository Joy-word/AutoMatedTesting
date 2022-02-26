using System;
using System.Collections.Generic;
using System.Globalization;
using System.Text;
using System.Windows;
using System.Windows.Data;

namespace AutoMatedDataModifier.Converts {
    public class ViewVisibleConvert : IValueConverter {
        public object Convert(object value, Type targetType, object parameter, CultureInfo culture) {
            if (value != null) {
                string valueStr = value.ToString();
                if (parameter != null) {
                    string paraStr = parameter.ToString();
                    if (paraStr == "LocationXY") {
                        return valueStr == "absolute" ? Visibility.Visible : Visibility.Collapsed;
                    }
                    else if (paraStr == "VisualImagePath") {
                        return valueStr == "visualization" ? Visibility.Visible : Visibility.Collapsed;
                    }
                    else if(paraStr == "ActionParam") {
                        return valueStr == "mouse_move" ? Visibility.Collapsed : Visibility.Visible;
                    }
                    else {
                        return Visibility.Visible;
                    }
                }
                else {
                    return Visibility.Visible;
                }
            }
            return Visibility.Collapsed;
        }

        public object ConvertBack(object value, Type targetType, object parameter, CultureInfo culture) {
            return new object();
        }
    }
}
