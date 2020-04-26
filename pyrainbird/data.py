_DEFAULT_PAGE = 0


class Pageable(object):
    def __init__(self, page=_DEFAULT_PAGE):
        self.page = page

    def __hash__(self):
        return hash(self.page)

    def __eq__(self, o):
        return isinstance(o, Pageable) and self.page == o.page

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "page: %d" % self.page


class Echo(object):
    def __init__(self, echo):
        self.echo = echo

    def __hash__(self):
        return hash(self.echo)

    def __eq__(self, o):
        return isinstance(o, Echo) and self.echo == o.echo

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "echo: %02X" % self.echo


class CommandSupport(Echo):
    def __init__(self, support, echo=0):
        super(CommandSupport, self).__init__(echo)
        self.support = support

    def __eq__(self, o):
        return (
            super(CommandSupport, self).__eq__(o)
            and isinstance(o, CommandSupport)
            and o.support == self.support
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __hash__(self):
        return hash((super(CommandSupport, self).__hash__(), self.support))

    def __str__(self):
        return "command support: %02X, %s" % (
            self.support,
            super(CommandSupport, self).__str__(),
        )


class ModelAndVersion(object):
    def __init__(self, model, revMajor, revMinor):
        self.model = model
        self.major = revMajor
        self.minor = revMinor

    def __hash__(self):
        return hash((self.model, self.major, self.minor))

    def __eq__(self, o):
        return (
            isinstance(o, ModelAndVersion)
            and self.model == o.model
            and self.major == o.major
            and self.minor == o.minor
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "model: %04X, version: %d.%d" % (
            self.model,
            self.major,
            self.minor,
        )


class States(object):
    def __init__(self, mask="0000"):
        self.count = len(mask) * 4
        self.mask = int(mask, 16)
        self.states = ()
        rest = mask
        while rest:
            current = int(rest[:2], 16)
            rest = rest[2:]
            for i in range(0, 8):
                self.states = self.states + (bool((1 << i) & current),)

    def active(self, number):
        return self.states[number - 1]

    def __hash__(self):
        return hash((self.count, self.mask, self.states))

    def __eq__(self, o):
        return (
            isinstance(o, States)
            and self.count == o.count
            and self.mask == o.mask
            and self.states == o.states
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        result = ()
        for i in range(0, self.count):
            result += ("%d:%d" % (i + 1, 1 if self.states[i] else 0),)
        return "states: %s" % ", ".join(result)


class AvailableStations(Pageable):
    def __init__(self, mask, page=_DEFAULT_PAGE):
        super(AvailableStations, self).__init__(page)
        self.stations = States(mask)

    def __hash__(self):
        return hash((super(AvailableStations, self).__hash__(), self.stations))

    def __eq__(self, o):
        return (
            super(AvailableStations, self).__eq__(o)
            and isinstance(o, AvailableStations)
            and self.stations == o.stations
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "available stations: %X, %s" % (
            self.stations.mask,
            super(AvailableStations, self).__str__(),
        )


class WaterBudget(object):
    def __init__(self, program, adjust):
        self.program = program
        self.adjust = adjust

    def __hash__(self):
        return hash((self.program, self.adjust))

    def __eq__(self, o):
        return (
            isinstance(o, WaterBudget)
            and self.program == o.program
            and self.adjust == o.adjust
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "Water budget: program: %d, hi: %02X" % (
            self.program,
            self.adjust,
        )

class ZoneSchedule(object):
    # "zone", "duration", "StartTime1inHoursFromMidnightInMinutesDividedByTen",
    # "StartTime2inHoursFromMidnightInMinutesDividedByTen","StartTime3inHoursFromMidnightInMinutesDividedByTen",
    # "StartTime4inHoursFromMidnightInMinutesDividedByTen", "StartTime5inHoursFromMidnightInMinutesDividedByTen",
    # "StartTime6inHoursFromMidnightInMinutesDividedByTen","PersonalizzatoDispariPariCiclico",
    # "FrequencyInBinaryStartingFromSunday","DaysCycle", "RemainingDays"
    def __init__(self, zone, duration, startTime1, startTime2, startTime3, startTime4, startTime5, startTime6, 
                       scheduleType, frequency, dayCycle, remainingDays):
        self.zone = zone
        self.duration = duration
        self.startTime1 = "" if startTime1 == 144 else str(int((startTime1 * 1) / 6)).zfill(2) + ":" + str((startTime1 * 10) % 60).zfill(2)
        self.startTime2 = "" if startTime2 == 144 else str(int((startTime2 * 1) / 6)).zfill(2) + ":" + str((startTime2 * 10) % 60).zfill(2)
        self.startTime3 = "" if startTime3 == 144 else str(int((startTime3 * 1) / 6)).zfill(2) + ":" + str((startTime3 * 10) % 60).zfill(2)
        self.startTime4 = "" if startTime4 == 144 else str(int((startTime4 * 1) / 6)).zfill(2) + ":" + str((startTime4 * 10) % 60).zfill(2)
        self.startTime5 = "" if startTime5 == 144 else str(int((startTime5 * 1) / 6)).zfill(2) + ":" + str((startTime5 * 10) % 60).zfill(2)
        self.startTime6 = "" if startTime6 == 144 else str(int((startTime6 * 1) / 6)).zfill(2) + ":" + str((startTime6 * 10) % 60).zfill(2)
        self.scheduleType = scheduleType
        self.frequency = frequency
        self.isSundayScheduled = True if self.get_bit(frequency, 0) == 1 else False
        self.isMondayScheduled = True if self.get_bit(frequency, 1) == 1 else False
        self.isTuesdayScheduled = True if self.get_bit(frequency, 2) == 1 else False
        self.isWednesdayScheduled = True if self.get_bit(frequency, 3) == 1 else False
        self.isThursdayScheduled = True if self.get_bit(frequency, 4) == 1 else False
        self.isFridayScheduled = True if self.get_bit(frequency, 5) == 1 else False
        self.isSaturdayScheduled = True if self.get_bit(frequency, 6) == 1 else False
        self.dayCycle = dayCycle
        self.remainingDays = remainingDays

    def get_bit(self, byteval,idx):
        return ((byteval&(1<<idx))!=0)

    def __hash__(self):
        return hash((self.zone, self.duration, self.startTime1, self.startTime2, self.startTime3, self.startTime4, 
                     self.startTime5, self.startTime6, self.scheduleType, self.frequency, self.dayCycle, self.remainingDays))

    def __eq__(self, o):
        return (
            isinstance(o, ZoneSchedule)
            and self.zone == o.zone
            and self.duration == o.duration
            and self.startTime1 == o.startTime1
            and self.startTime2 == o.startTime2
            and self.startTime3 == o.startTime3
            and self.startTime4 == o.startTime4
            and self.startTime5 == o.startTime5
            and self.startTime6 == o.startTime6
            and self.scheduleType == o.scheduleType
            and self.frequency == o.frequency
            and self.dayCycle == o.dayCycle
            and self.remainingDays == o.remainingDays
        )

    def __ne__(self, o):
        return not __eq__(o)

    def __str__(self):
        return "Zone schedule : zone: %d, duration: %d, startTime1: %s, startTime2: %s, startTime3: %s, startTime4: %s, startTime5: %s, startTime6: %s, scheduleType: %d, frequency: %d [Sun: %d, Mon: %d, Tue: %d, Wed: %d, Thu: %d, Fri: %d, Sat: %d], dayCycle: %d, remainingDays: %d" % (
            self.zone,
            self.duration,
            self.startTime1,
            self.startTime2,
            self.startTime3,
            self.startTime4,
            self.startTime5,
            self.startTime6,
            self.scheduleType,
            self.frequency,
            self.isSundayScheduled,
            self.isMondayScheduled,
            self.isTuesdayScheduled,
            self.isWednesdayScheduled,
            self.isThursdayScheduled,
            self.isFridayScheduled,
            self.isSaturdayScheduled,            
            self.dayCycle,
            self.remainingDays
        )
