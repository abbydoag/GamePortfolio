namespace AnimalMatchingGame;

public partial class MainPage : ContentPage
{

	public MainPage()
	{
		InitializeComponent();
	}

    private void PlayAgainButton_Clicked(object sender, EventArgs e)
    {
        AnimalButtons.IsVisible = true;
        PlayAgainButton.IsVisible = false;

        List<String> animalEmoji = [
            "🐝", "🐝",
            "🦌", "🦌",
            "🦈", "🦈",
            "🦖", "🦖",
            "🐦‍🔥", "🐦‍🔥",
            "🦦", "🦦",
            "🦣", "🦣",
            "🐕‍🦺", "🐕‍🦺"
        ];

        //Añadir a cada botón
        foreach (var button in AnimalButtons.Children.OfType<Button>())
        {
            int index = Random.Shared.Next(animalEmoji.Count);
            string nextEmoji = animalEmoji[index];
            button.Text = nextEmoji;
            animalEmoji.RemoveAt(index);
        }

        Dispatcher.StartTimer(TimeSpan.FromSeconds(.1), TimerTick);
    }
    
    int tenthsOfSecondsElapsed = 0;
    private bool TimerTick()
    {     
        if(!this.IsLoaded) return false;
        tenthsOfSecondsElapsed++;
        TimeElapsed.Text = "Time Elapsed: "+(tenthsOfSecondsElapsed/10F).ToString("0.0s");

        if (PlayAgainButton.IsVisible)
        {
            tenthsOfSecondsElapsed = 0;
            return false;
        }
        return true;
    }


    Button lastClicked;
    bool findingMatch = false;
    int matchesFound = 0;
    private void ButtonGame_Clicked(object sender, EventArgs e)
    {
        if (sender is Button buttonGame_Clicked)
        {
            if(!string.IsNullOrWhiteSpace(buttonGame_Clicked.Text) && (findingMatch == false))
            {
                buttonGame_Clicked.BackgroundColor = Colors.Red;
                lastClicked = buttonGame_Clicked;
                findingMatch = true;
            }
            else
            {
                if ((buttonGame_Clicked != lastClicked) && (buttonGame_Clicked.Text == lastClicked.Text)
                && (!String.IsNullOrWhiteSpace(buttonGame_Clicked.Text)))
                {
                    matchesFound++;
                    lastClicked.Text = " ";
                    buttonGame_Clicked.Text = " ";
                }
                lastClicked.BackgroundColor = Colors.LightBlue;
                buttonGame_Clicked.BackgroundColor = Colors.LightBlue;
                findingMatch = false;
            }
        }
        if (matchesFound == 8)
        {
            matchesFound = 0;
            AnimalButtons.IsVisible = false;
            PlayAgainButton.IsVisible = true;
        }
    }
}